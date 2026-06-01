# app/routers/feed.py
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
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


@router.post("/api/feed/refresh", response_class=JSONResponse)
async def refresh_feed(db: Session = Depends(get_db)):
    """Manually trigger a feed refresh and AI processing."""
    new_articles = feed_service.fetch_all(db)
    processed = ai_processing_service.process_unprocessed(db, limit=20)
    return {"status": "ok", "new_articles": new_articles, "ai_processed": processed}
