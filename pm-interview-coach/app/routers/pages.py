"""pm-interview-coach/app/routers/pages.py"""
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.attempt import Attempt
from app.models.question import Question

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


def _ctx(request: Request, **kwargs: object) -> dict[str, object]:
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


@router.get("/", response_class=HTMLResponse)
async def landing(request: Request, db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    categories = await _fetch_category_stats(db)
    return templates.TemplateResponse(
        "index.html",
        _ctx(
            request,
            title="PM Interview Coach",
            current_page="/",
            categories=categories,
        ),
    )


@router.get("/history", response_class=HTMLResponse)
async def history(
    request: Request,
    category: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    attempts = await _fetch_attempts(db, category, min_score, max_score)
    categories = await _fetch_category_list(db)
    return templates.TemplateResponse(
        "history.html",
        _ctx(
            request,
            title="Practice History",
            current_page="/history",
            attempts=attempts,
            categories=categories,
            selected_category=category or "",
            min_score=min_score,
            max_score=max_score,
        ),
    )


async def _fetch_category_stats(db: AsyncSession) -> list[dict[str, object]]:
    query = (
        select(Question.category, func.count(Question.id), func.avg(Attempt.overall_score))
        .select_from(Question)
        .join(Attempt, Attempt.question_id == Question.id, isouter=True)
        .group_by(Question.category)
        .order_by(Question.category)
    )
    result = await db.execute(query)
    stats = []
    for row in result.all():
        stats.append(
            {
                "category": row[0],
                "label": _format_category(row[0]),
                "count": int(row[1] or 0),
                "avg_score": float(row[2]) if row[2] is not None else 0.0,
            }
        )
    return stats


async def _fetch_category_list(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(Question.category).distinct().order_by(Question.category)
    )
    return [row[0] for row in result.all()]


async def _fetch_attempts(
    db: AsyncSession,
    category: Optional[str],
    min_score: Optional[float],
    max_score: Optional[float],
) -> list[dict[str, object]]:
    query = (
        select(
            Attempt,
            Question.question_text,
            Question.category,
        )
        .join(Question, Attempt.question_id == Question.id)
        .order_by(Attempt.created_at.desc())
        .limit(50)
    )
    if category:
        query = query.where(Question.category == category)
    if min_score is not None:
        query = query.where(Attempt.overall_score >= min_score)
    if max_score is not None:
        query = query.where(Attempt.overall_score <= max_score)

    result = await db.execute(query)
    attempts = []
    for attempt, question_text, question_category in result.all():
        attempts.append(
            {
                "date": attempt.created_at,
                "category": question_category,
                "question_text": question_text,
                "score": attempt.overall_score,
                "time_spent_sec": attempt.time_spent_sec,
            }
        )
    return attempts


def _format_category(category: str) -> str:
    return category.replace("_", " ").title()
