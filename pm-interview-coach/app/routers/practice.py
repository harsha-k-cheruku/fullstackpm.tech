"""pm-interview-coach/app/routers/practice.py"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.attempt import Attempt
from app.models.question import Question
from app.models.session import PracticeSession
from app.services.evaluator import EvaluationError, evaluate_answer
from app.services.question_selector import get_random_question

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

router = APIRouter()


def _ctx(request: Request, **kwargs: object) -> dict[str, object]:
    return {"request": request, "config": settings, **kwargs}


@router.get("/practice/random", response_class=HTMLResponse)
async def practice_random(request: Request, db: AsyncSession = Depends(get_db)) -> HTMLResponse:
    question = await get_random_question(db)
    if question is None:
        raise HTTPException(status_code=404, detail="No questions available")
    return await _render_practice(request, db, question, None)


@router.get("/practice/{category}", response_class=HTMLResponse)
async def practice_category(
    request: Request, category: str, db: AsyncSession = Depends(get_db)
) -> HTMLResponse:
    question = await get_random_question(db, category)
    if question is None:
        raise HTTPException(status_code=404, detail="No questions available")
    return await _render_practice(request, db, question, category)


@router.post("/api/practice/submit", response_class=HTMLResponse)
async def submit_answer(
    request: Request,
    question_id: int = Form(...),
    session_id: str = Form(...),
    answer_text: str = Form(...),
    time_spent_sec: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db),
) -> HTMLResponse:
    if len(answer_text.strip()) < 50:
        return templates.TemplateResponse(
            "partials/feedback.html",
            _ctx(
                request,
                evaluation=None,
                error_message="Answer must be at least 50 characters.",
            ),
        )

    question = await db.get(Question, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    try:
        evaluation = await evaluate_answer(
            category=question.category,
            question=question.question_text,
            answer=answer_text,
            time_spent_sec=time_spent_sec,
        )
    except EvaluationError as exc:
        return templates.TemplateResponse(
            "partials/feedback.html",
            _ctx(request, evaluation=None, error_message=str(exc)),
        )

    attempt = Attempt(
        question_id=question.id,
        session_id=session_id,
        answer_text=answer_text,
        time_spent_sec=time_spent_sec,
        overall_score=evaluation.overall_score,
        framework_score=evaluation.framework_score,
        structure_score=evaluation.structure_score,
        completeness_score=evaluation.completeness_score,
        strengths=json.dumps(evaluation.strengths),
        improvements=json.dumps(evaluation.improvements),
        suggested_framework=evaluation.suggested_framework,
        example_point=evaluation.example_point,
        raw_eval_json=evaluation.raw_json,
        created_at=datetime.now(timezone.utc),
    )
    db.add(attempt)
    await db.commit()

    await _update_session_stats(db, session_id)

    return templates.TemplateResponse(
        "partials/feedback.html",
        _ctx(request, evaluation=evaluation, error_message=None),
    )


async def _render_practice(
    request: Request,
    db: AsyncSession,
    question: Question,
    category: Optional[str],
) -> HTMLResponse:
    session_id = str(uuid4())
    session = PracticeSession(
        id=session_id, category_filter=category or question.category
    )
    db.add(session)
    await db.commit()

    return templates.TemplateResponse(
        "practice.html",
        _ctx(
            request,
            title="Practice — PM Interview Coach",
            current_page="",
            question=question,
            session_id=session_id,
        ),
    )


async def _update_session_stats(db: AsyncSession, session_id: str) -> None:
    session = await db.get(PracticeSession, session_id)
    if session is None:
        return

    result = await db.execute(
        select(func.count(Attempt.id), func.avg(Attempt.overall_score)).where(
            Attempt.session_id == session_id
        )
    )
    row = result.first()
    if not row:
        return

    session.questions_count = int(row[0] or 0)
    session.avg_score = float(row[1]) if row[1] is not None else None
    await db.commit()
