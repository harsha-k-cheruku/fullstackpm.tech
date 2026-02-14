"""pm-interview-coach/app/routers/api.py"""
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.attempt import Attempt
from app.models.question import Question
from app.services.question_selector import get_random_question
from app.services.stats_engine import StatsEngine

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


def _ctx(request: Request, **kwargs: object) -> dict[str, object]:
    return {"request": request, "config": settings, **kwargs}


@router.get("/partials/question-card/{question_id}", response_class=HTMLResponse)
async def question_card(
    request: Request, question_id: int, db: AsyncSession = Depends(get_db)
) -> HTMLResponse:
    current = await db.get(Question, question_id)
    if current is None:
        return templates.TemplateResponse(
            "partials/question_card.html",
            _ctx(request, question=None),
        )

    next_question = await _next_question(db, current)
    return templates.TemplateResponse(
        "partials/question_card.html",
        _ctx(request, question=next_question or current),
    )


@router.post("/partials/feedback", response_class=HTMLResponse)
async def feedback_reset(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "partials/feedback.html",
        _ctx(request, evaluation=None, error_message=None),
    )


@router.get("/partials/history-table", response_class=HTMLResponse)
async def history_table(
    request: Request,
    category: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    attempts = await _fetch_attempts(db, category, min_score, max_score)
    return templates.TemplateResponse(
        "partials/history_table.html",
        _ctx(request, attempts=attempts),
    )


@router.get("/partials/stats-cards", response_class=HTMLResponse)
async def stats_cards(request: Request, db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    stats = StatsEngine(db)
    overview = await stats.overview()
    return templates.TemplateResponse(
        "partials/stats_cards.html",
        _ctx(request, overview=overview),
    )


async def _next_question(db: AsyncSession, current: Question) -> Question | None:
    for _ in range(3):
        candidate = await get_random_question(db, current.category)
        if candidate and candidate.id != current.id:
            return candidate
    return current


async def _fetch_attempts(
    db: AsyncSession,
    category: Optional[str],
    min_score: Optional[float],
    max_score: Optional[float],
) -> list[dict[str, object]]:
    query = (
        select(Attempt, Question.question_text, Question.category)
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
