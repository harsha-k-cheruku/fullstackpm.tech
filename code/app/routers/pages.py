# app/routers/pages.py
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
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
    content_service = request.app.state.content_service
    reading_service = request.app.state.reading_service
    recent_posts, _ = content_service.get_posts(page=1, per_page=3)
    reading = reading_service.get()
    return templates.TemplateResponse(
        "index.html",
        _ctx(
            request,
            title="@fullstackpm - Harsha Cheruku",
            current_page="/",
            recent_posts=recent_posts,
            reading=reading,
        ),
    )


@router.get("/about")
async def about(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/@fullstackpm", status_code=301)


@router.get("/contact")
async def contact(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/@fullstackpm", status_code=301)


@router.get("/resume", response_class=HTMLResponse)
async def resume(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resume.html",
        _ctx(request, title="Resume — fullstackpm.tech", current_page="/resume"),
    )


@router.get("/tools/upstart-clearing-simulator", response_class=HTMLResponse)
async def upstart_clearing_simulator(request: Request) -> FileResponse:
    """Serve the Upstart Clearing Simulator — interactive tool for marketplace clearing mechanics."""
    return FileResponse(str(settings.static_dir / "tools" / "upstart_clearing_simulator.html"))


@router.get("/tools/upstart-data-methods", response_class=HTMLResponse)
async def upstart_data_methods(request: Request) -> FileResponse:
    """Serve Data & Methods companion page for the Upstart Clearing Simulator."""
    return FileResponse(str(settings.static_dir / "tools" / "upstart_data_methods.html"))


@router.get("/@fullstackpm", response_class=HTMLResponse)
async def fullstackpm_page(request: Request) -> HTMLResponse:
    """Personal brand page — consolidated about/contact/career."""
    return templates.TemplateResponse(
        "fullstackpm.html",
        _ctx(request, title="@fullstackpm — Harsha Cheruku", current_page="/@fullstackpm"),
    )
