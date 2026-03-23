# app/routers/likes.py
import uuid
from datetime import datetime
from typing import Optional, Tuple

from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import SessionLocal
from app.models.like import Like

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

_COOKIE = "blog_visitor_id"
_COOKIE_MAX_AGE = 365 * 24 * 60 * 60  # 1 year


def _ctx(request: Request, **kwargs) -> dict:
    return {"request": request, "config": settings, "year": datetime.now().year, **kwargs}


def _like_state(slug: str, visitor_id: Optional[str]) -> Tuple[int, bool]:
    """Return (count, liked) for slug + visitor."""
    db = SessionLocal()
    count = db.query(Like).filter(Like.blog_post_slug == slug).count()
    liked = bool(visitor_id and db.query(Like).filter(
        Like.blog_post_slug == slug,
        Like.user_id == visitor_id,
    ).first())
    db.close()
    return count, liked


@router.post("/api/blog/{slug}/like", response_class=HTMLResponse)
async def toggle_like(
    slug: str,
    request: Request,
    blog_visitor_id: str = Cookie(default=None),
) -> HTMLResponse:
    """Toggle like. Creates visitor cookie on first interaction."""
    # Assign a visitor ID if this is their first time
    is_new_visitor = not blog_visitor_id
    if is_new_visitor:
        blog_visitor_id = str(uuid.uuid4())

    db = SessionLocal()
    try:
        existing = db.query(Like).filter(
            Like.blog_post_slug == slug,
            Like.user_id == blog_visitor_id,
        ).first()

        if existing:
            db.delete(existing)
            db.commit()
            liked = False
        else:
            db.add(Like(blog_post_slug=slug, user_id=blog_visitor_id))
            db.commit()
            liked = True

        count = db.query(Like).filter(Like.blog_post_slug == slug).count()
    except IntegrityError:
        db.rollback()
        liked = True
        count = db.query(Like).filter(Like.blog_post_slug == slug).count()
    finally:
        db.close()

    response = templates.TemplateResponse(
        "partials/like_button.html",
        _ctx(request, slug=slug, liked=liked, like_count=count),
    )
    if is_new_visitor:
        response.set_cookie(
            _COOKIE, blog_visitor_id,
            max_age=_COOKIE_MAX_AGE,
            httponly=True,
            samesite="lax",
        )
    return response
