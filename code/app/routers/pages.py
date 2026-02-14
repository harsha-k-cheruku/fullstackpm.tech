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
    return templates.TemplateResponse(
        "home.html",
        _ctx(request, title="Harsha Cheruku — Full Stack AI PM", current_page="/"),
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "about.html",
        _ctx(request, title="About — fullstackpm.tech", current_page="/about"),
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "contact.html",
        _ctx(request, title="Contact — fullstackpm.tech", current_page="/contact"),
    )


@router.get("/resume", response_class=HTMLResponse)
async def resume(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resume.html",
        _ctx(request, title="Resume — fullstackpm.tech", current_page="/resume"),
    )
