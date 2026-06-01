# app/routers/feed.py
from datetime import datetime
from html import escape

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.feed_article import FeedArticle
from app.services.ai_processing_service import ai_processing_service
from app.services.brief_service import brief_service
from app.services.feed_service import feed_service

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

CATEGORIES = [
    ("all", "All"),
    ("pm", "Product"),
    ("engineering", "Engineering"),
    ("strategy", "Strategy"),
    ("ai", "AI & Research"),
]


def _check_editorial_token(token: str):
    if not token or token != settings.editorial_token:
        raise HTTPException(status_code=403, detail="Invalid editorial token")


@router.get("/feed", response_class=HTMLResponse)
async def feed_page(request: Request, category: str = "all", db: Session = Depends(get_db)):
    articles = feed_service.get_articles(db, category=category)
    return templates.TemplateResponse(
        "feed/index.html",
        {
            "request": request,
            "config": settings,
            "year": datetime.now().year,
            "title": "PM Intelligence Feed — fullstackpm.tech",
            "current_page": "/feed",
            "articles": articles,
            "active_category": category,
            "categories": CATEGORIES,
        },
    )


@router.get("/feed/article/{article_id}", response_class=HTMLResponse)
async def article_page(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = feed_service.get_article(db, article_id)
    if not article or article.is_dismissed:
        raise HTTPException(status_code=404, detail="Article not found")
    insight_label = {
        "engineering": "PM Take",
        "strategy": "First Principle",
        "pm": "Takeaway",
        "ai": "AI for PMs",
    }.get(article.source_category, "Insight")
    insight = article.ai_summary or article.first_principle or article.key_insight or article.ai_insight
    return templates.TemplateResponse(
        "feed/article.html",
        {
            "request": request,
            "config": settings,
            "year": datetime.now().year,
            "title": f"{article.title} — fullstackpm.tech",
            "current_page": "/feed",
            "article": article,
            "insight": insight,
            "insight_label": insight_label,
        },
    )


@router.get("/feed/editorial", response_class=HTMLResponse)
async def editorial_page(request: Request, token: str = "", db: Session = Depends(get_db)):
    """Editorial dashboard — token-gated."""
    _check_editorial_token(token)
    articles = (
        db.query(FeedArticle)
        .filter(FeedArticle.is_dismissed == False)
        .order_by(
            FeedArticle.is_editors_pick.desc(),
            FeedArticle.ai_score.desc().nullslast(),
            FeedArticle.fetched_at.desc(),
        )
        .limit(100)
        .all()
    )
    total = db.query(FeedArticle).count()
    processed = db.query(FeedArticle).filter(FeedArticle.ai_processed_at.isnot(None)).count()
    picks = db.query(FeedArticle).filter(FeedArticle.is_editors_pick == True).count()
    return templates.TemplateResponse(
        "feed/editorial.html",
        {
            "request": request,
            "config": settings,
            "year": datetime.now().year,
            "title": "Editorial Dashboard — fullstackpm.tech",
            "current_page": "/feed/editorial",
            "articles": articles,
            "token": token,
            "stats": {"total": total, "processed": processed, "picks": picks},
        },
    )


@router.post("/api/feed/refresh", response_class=JSONResponse)
async def refresh_feed(db: Session = Depends(get_db)):
    """Manually trigger a feed refresh and AI processing."""
    new_articles = feed_service.fetch_all(db)
    processed = ai_processing_service.process_unprocessed(db, limit=20)
    return {"status": "ok", "new_articles": new_articles, "ai_processed": processed}


@router.post("/api/feed/brief/generate", response_class=JSONResponse)
async def generate_brief(token: str = "", db: Session = Depends(get_db)):
    """Manually trigger a fresh audio brief generation."""
    _check_editorial_token(token)
    success = await brief_service.generate(db)
    latest = brief_service.get_latest()
    return {
        "status": "ok" if success else "error",
        "generated": success,
        "latest": latest,
    }


@router.get("/pm-brief.xml")
async def podcast_rss():
    """Podcast RSS feed for PM Daily Brief."""
    episodes = brief_service.get_all()
    items = ""
    for episode in episodes:
        pub_date = ""
        try:
            generated_at = datetime.fromisoformat(episode.get("generated_at", ""))
            pub_date = generated_at.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except Exception:
            pass
        audio_url = episode.get("audio_url", "")
        title = escape(episode.get("title", ""))
        description = escape(f"{episode.get('article_count', 0)} top PM stories, scored and distilled.")
        escaped_audio_url = escape(audio_url, quote=True)
        items += f"""
    <item>
      <title>{title}</title>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{escaped_audio_url}" type="audio/mpeg"/>
      <guid>{escaped_audio_url}</guid>
    </item>"""

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>PM Daily Brief</title>
    <link>https://fullstackpm.tech</link>
    <description>Daily intelligence brief for product managers — top stories from PM, engineering, strategy, and AI, distilled to essentials by fullstackpm.tech.</description>
    <language>en-us</language>
    <itunes:author>Harsha Cheruku</itunes:author>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="https://fullstackpm.tech/static/img/FSPM.png"/>
    <image>
      <url>https://fullstackpm.tech/static/img/FSPM.png</url>
      <title>PM Daily Brief</title>
      <link>https://fullstackpm.tech</link>
    </image>{items}
  </channel>
</rss>"""
    return Response(content=rss, media_type="application/rss+xml")


@router.post("/api/feed/article/{article_id}/pick", response_class=HTMLResponse)
async def toggle_pick(article_id: int, token: str = "", db: Session = Depends(get_db)):
    """Toggle is_editors_pick. Returns updated button HTML for HTMX swap."""
    _check_editorial_token(token)
    article = db.query(FeedArticle).filter(FeedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_editors_pick = not article.is_editors_pick
    db.commit()
    label = "Featured" if article.is_editors_pick else "Feature It"
    color = "var(--color-accent)" if article.is_editors_pick else "var(--color-text-tertiary)"
    return HTMLResponse(
        f'<button hx-post="/api/feed/article/{article_id}/pick?token={token}" '
        f'hx-target="this" hx-swap="outerHTML" '
        f'style="background:none;border:1px solid {color};color:{color};padding:4px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem;font-weight:600;">'
        f"{label}</button>"
    )


@router.post("/api/feed/article/{article_id}/dismiss", response_class=HTMLResponse)
async def dismiss_article(article_id: int, token: str = "", db: Session = Depends(get_db)):
    """Mark article as dismissed. Returns empty string to remove card from HTMX view."""
    _check_editorial_token(token)
    article = db.query(FeedArticle).filter(FeedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_dismissed = True
    db.commit()
    return HTMLResponse("")
