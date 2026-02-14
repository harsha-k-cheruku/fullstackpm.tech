"""pm-interview-coach/app/routers/stats.py"""
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.services.stats_engine import StatsEngine

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


def _ctx(request: Request, **kwargs: object) -> dict[str, object]:
    return {"request": request, "config": settings, **kwargs}


@router.get("/progress", response_class=HTMLResponse)
async def progress(request: Request, db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    stats = StatsEngine(db)
    overview = await stats.overview()
    return templates.TemplateResponse(
        "progress.html",
        _ctx(
            request,
            title="Progress Dashboard",
            current_page="/progress",
            overview=overview,
        ),
    )


@router.get("/api/stats/overview", response_class=JSONResponse)
async def stats_overview(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    stats = StatsEngine(db)
    return JSONResponse(await stats.overview())


@router.get("/api/stats/by-category", response_class=JSONResponse)
async def stats_by_category(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    stats = StatsEngine(db)
    return JSONResponse(await stats.by_category())


@router.get("/api/stats/trend", response_class=JSONResponse)
async def stats_trend(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    stats = StatsEngine(db)
    return JSONResponse(await stats.trend())


@router.get("/api/stats/heatmap", response_class=JSONResponse)
async def stats_heatmap(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    stats = StatsEngine(db)
    return JSONResponse(await stats.heatmap())
