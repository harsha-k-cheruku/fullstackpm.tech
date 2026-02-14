# app/routers/blog.py
from datetime import datetime

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.comment import Comment

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def _ctx(request: Request, **kwargs) -> dict:
    """Build the standard template context."""
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


@router.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request, page: int = Query(1, ge=1)) -> HTMLResponse:
    content_service = request.app.state.content_service
    posts, total = content_service.get_posts(page=page, per_page=10)
    tags = content_service.get_all_tags()
    has_newer = page > 1
    has_older = page * 10 < total

    return templates.TemplateResponse(
        "blog/list.html",
        _ctx(
            request,
            title="Blog  fullstackpm.tech",
            current_page="/blog",
            posts=posts,
            tags=tags,
            page=page,
            has_newer=has_newer,
            has_older=has_older,
        ),
    )


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_detail(request: Request, slug: str) -> HTMLResponse:
    content_service = request.app.state.content_service
    post = content_service.get_post_by_slug(slug)
    if post is None:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Page Not Found", current_page=""),
            status_code=404,
        )

    # Fetch comments from database
    db = SessionLocal()
    comments = (
        db.query(Comment)
        .filter(Comment.blog_post_slug == slug)
        .order_by(Comment.created_at.desc())
        .all()
    )
    db.close()

    return templates.TemplateResponse(
        "blog/detail.html",
        _ctx(
            request,
            title=f"{post.title}  Blog",
            current_page="/blog",
            post=post,
            comments=comments,
        ),
    )


@router.get("/blog/tag/{tag}", response_class=HTMLResponse)
async def blog_tag(request: Request, tag: str, page: int = Query(1, ge=1)) -> HTMLResponse:
    content_service = request.app.state.content_service
    posts, total = content_service.get_posts_by_tag(tag, page=page, per_page=10)
    tags = content_service.get_all_tags()
    has_newer = page > 1
    has_older = page * 10 < total

    return templates.TemplateResponse(
        "blog/tag.html",
        _ctx(
            request,
            title=f"{tag}  Blog",
            current_page="/blog",
            posts=posts,
            tags=tags,
            tag=tag,
            page=page,
            has_newer=has_newer,
            has_older=has_older,
        ),
    )


# HTMX Endpoints
@router.get("/api/blog/posts", response_class=HTMLResponse)
async def blog_posts_htmx(request: Request, page: int = Query(1, ge=1)) -> HTMLResponse:
    """HTMX endpoint for loading more blog posts."""
    content_service = request.app.state.content_service
    posts, total = content_service.get_posts(page=page, per_page=10)
    has_older = page * 10 < total

    return templates.TemplateResponse(
        "blog/partials/post_list.html",
        _ctx(
            request,
            posts=posts,
            page=page,
            has_older=has_older,
        ),
    )
