# app/routers/marketplace.py
from __future__ import annotations

import csv
from datetime import datetime
from io import StringIO

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.analytics import get_snapshot

router = APIRouter(prefix="/tools/marketplace-analytics")
templates = Jinja2Templates(directory=str(settings.templates_dir))


def _ctx(request: Request, **kwargs) -> dict:
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


def _parse_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


def _filters(request: Request) -> dict:
    date_range = _parse_int(request.query_params.get("date_range"), 90)
    category = request.query_params.get("category", "all")
    sort_by = request.query_params.get("sort_by", "revenue")
    sort_dir = request.query_params.get("sort_dir", "desc")
    return {
        "date_range": date_range,
        "category": category,
        "sort_by": sort_by,
        "sort_dir": sort_dir,
    }


@router.get("", response_class=HTMLResponse)
async def marketplace_dashboard(request: Request) -> HTMLResponse:
    filters = _filters(request)
    snapshot = get_snapshot(
        date_range_days=filters["date_range"],
        category=filters["category"],
        sort_by=filters["sort_by"],
        sort_dir=filters["sort_dir"],
    )
    return templates.TemplateResponse(
        "marketplace-analytics/index.html",
        _ctx(
            request,
            title="Marketplace Analytics — fullstackpm.tech",
            current_page="/tools/marketplace-analytics",
            snapshot=snapshot,
            **filters,
        ),
    )


@router.get("/partials/dashboard", response_class=HTMLResponse)
async def marketplace_dashboard_partial(request: Request) -> HTMLResponse:
    filters = _filters(request)
    snapshot = get_snapshot(
        date_range_days=filters["date_range"],
        category=filters["category"],
        sort_by=filters["sort_by"],
        sort_dir=filters["sort_dir"],
    )
    return templates.TemplateResponse(
        "marketplace-analytics/partials/dashboard.html",
        _ctx(request, snapshot=snapshot, **filters),
    )


@router.get("/export")
async def export_category_data(request: Request) -> StreamingResponse:
    filters = _filters(request)
    snapshot = get_snapshot(
        date_range_days=filters["date_range"],
        category=filters["category"],
        sort_by=filters["sort_by"],
        sort_dir=filters["sort_dir"],
    )

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Category", "Listings", "Revenue", "Avg Price", "Avg Rating"])
    for row in snapshot.categories:
        writer.writerow(
            [
                row.category,
                row.listings,
                f"{row.revenue:.2f}",
                f"{row.avg_price:.2f}",
                f"{row.avg_rating:.2f}",
            ]
        )

    buffer.seek(0)
    filename = "marketplace-category-performance.csv"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(buffer, media_type="text/csv", headers=headers)
