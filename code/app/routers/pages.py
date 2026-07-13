# app/routers/pages.py
from datetime import datetime
import json

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import SessionLocal
from app.services.brief_service import brief_service
from app.services.feed_service import feed_service

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
    db = SessionLocal()
    try:
        # Pick feature article: highest-scored across all categories (fallback to most recent)
        feature_pool = feed_service.get_articles(db, category="all", limit=1)
        feature = feature_pool[0] if feature_pool else None

        feature_id = feature.id if feature else None
        articles_by_category = {
            "pm":          [a for a in feed_service.get_articles(db, category="pm",          limit=4) if a.id != feature_id][:3],
            "engineering": [a for a in feed_service.get_articles(db, category="engineering", limit=4) if a.id != feature_id][:3],
            "strategy":    [a for a in feed_service.get_articles(db, category="strategy",    limit=4) if a.id != feature_id][:3],
            "ai":          [a for a in feed_service.get_articles(db, category="ai",          limit=4) if a.id != feature_id][:3],
        }
    finally:
        db.close()

    return templates.TemplateResponse(
        "index.html",
        _ctx(
            request,
            title="PM Intelligence — fullstackpm.tech",
            current_page="/",
            feature=feature,
            articles_by_category=articles_by_category,
            latest_brief=brief_service.get_latest(),
            today=datetime.now().strftime("%A · %B %-d, %Y").upper(),
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


@router.get("/tools/borrower_generation.js")
async def borrower_generation_js(request: Request) -> Response:
    """Serve shared borrower generation module for simulator + data & methods pages."""
    return FileResponse(
        str(settings.static_dir / "tools" / "borrower_generation.js"),
        media_type="application/javascript",
    )


@router.get("/miap-physics-research", response_class=HTMLResponse)
@router.get("/miap-physics-research.html", response_class=HTMLResponse)
async def miap_physics_research(request: Request) -> FileResponse:
    """MIAP B.Sc. Physics Honours research & career assessment poster."""
    return FileResponse(str(settings.static_dir / "tools" / "miap-physics-research.html"))


@router.get("/tools/lifecycle-simulator", response_class=HTMLResponse)
async def lifecycle_simulator(request: Request) -> HTMLResponse:
    """Lifecycle simulator for Upstart capital marketplace (5-tab interactive tool)."""
    return templates.TemplateResponse(
        "lifecycle_simulator.html",
        _ctx(request, title="Upstart Lifecycle Simulator — fullstackpm.tech", current_page="/tools/lifecycle-simulator"),
    )


@router.get("/reading/archive", response_class=HTMLResponse)
async def reading_archive(request: Request) -> HTMLResponse:
    """Archive view for previous PM reading stacks."""
    archive_file = settings.static_dir / "data" / "archives" / "reading_stack_2026_04.json"
    archive_data = {"last_updated": "", "picks": []}
    try:
        archive_data = json.loads(archive_file.read_text())
    except Exception:
        pass

    return templates.TemplateResponse(
        "reading_archive.html",
        _ctx(
            request,
            title="Reading Stack Archive — fullstackpm.tech",
            current_page="/reading/archive",
            archive=archive_data,
        ),
    )


@router.get("/@fullstackpm", response_class=HTMLResponse)
async def fullstackpm_page(request: Request) -> HTMLResponse:
    """Personal brand page — consolidated about/contact/career."""
    return templates.TemplateResponse(
        "fullstackpm.html",
        _ctx(request, title="@fullstackpm — Harsha Cheruku", current_page="/@fullstackpm"),
    )
