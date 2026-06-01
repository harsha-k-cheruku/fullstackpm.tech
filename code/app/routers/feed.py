# app/routers/feed.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.feed_article import FeedArticle
from app.services.ai_processing_service import ai_processing_service
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
