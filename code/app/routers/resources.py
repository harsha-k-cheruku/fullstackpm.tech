# app/routers/resources.py
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
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


@router.get("/resources/product-breakdowns", response_class=HTMLResponse)
async def product_breakdowns(request: Request) -> HTMLResponse:
    """Product Breakdowns placeholder page."""
    return templates.TemplateResponse(
        "resources/product_breakdowns.html",
        _ctx(
            request,
            title="Product Breakdowns - fullstackpm.tech",
            current_page="/resources/product-breakdowns",
        ),
    )


@router.get("/resources/ecosystem-maps", response_class=HTMLResponse)
async def ecosystem_maps(request: Request) -> HTMLResponse:
    """Ecosystem Maps gallery page."""
    return templates.TemplateResponse(
        "resources/ecosystem_maps.html",
        _ctx(
            request,
            title="Ecosystem Maps - fullstackpm.tech",
            current_page="/resources/ecosystem-maps",
        ),
    )


@router.get("/resources/ecosystem-maps/financial-ecosystem")
async def financial_ecosystem() -> FileResponse:
    """Serve the Financial Ecosystem visual map."""
    file_path = settings.static_dir / "resources" / "financial-ecosystem-v2.html"
    return FileResponse(file_path, media_type="text/html")
