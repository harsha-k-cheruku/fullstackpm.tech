# app/routers/pages.py
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

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


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Consolidated home page: Full Stack PM definition + components."""
    return templates.TemplateResponse(
        "index.html",
        _ctx(request, title="@fullstackpm - Harsha Cheruku", current_page="/"),
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    """Redirect to home for backward compatibility."""
    return templates.TemplateResponse(
        "index.html",
        _ctx(request, title="@fullstackpm - Harsha Cheruku", current_page="/"),
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request) -> HTMLResponse:
    """Redirect to home for backward compatibility."""
    return templates.TemplateResponse(
        "index.html",
        _ctx(request, title="@fullstackpm - Harsha Cheruku", current_page="/"),
    )


@router.get("/resume", response_class=HTMLResponse)
async def resume(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resume.html",
        _ctx(request, title="Resume — fullstackpm.tech", current_page="/resume"),
    )


@router.get("/@fullstackpm", response_class=HTMLResponse)
async def fullstackpm_page(request: Request) -> HTMLResponse:
    """Personal brand page — consolidated about/contact/career."""
    return templates.TemplateResponse(
        "fullstackpm.html",
        _ctx(request, title="@FullStackPM — Harsha Cheruku", current_page="/@fullstackpm"),
    )
