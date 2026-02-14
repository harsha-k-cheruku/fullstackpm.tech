# app/routers/interview_coach.py
"""Interview coach routes."""
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.interview_session import InterviewSession, InterviewAttempt
from app.services.interview_evaluator import evaluate_interview_answer

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

# Sample interview questions
INTERVIEW_QUESTIONS = {
    "product_design": [
        {
            "id": "pd_1",
            "text": "Design a feature to help users discover new restaurants on a food delivery app.",
            "category": "product_design",
        },
        {
            "id": "pd_2",
            "text": "How would you improve the onboarding experience for a productivity app?",
            "category": "product_design",
        },
    ],
    "strategy": [
        {
            "id": "st_1",
            "text": "Your company wants to enter the Indian market. How would you approach it?",
            "category": "strategy",
        },
        {
            "id": "st_2",
            "text": "What's your go-to-market strategy for a new AI writing assistant?",
            "category": "strategy",
        },
    ],
    "execution": [
        {
            "id": "ex_1",
            "text": "You have 3 months and a team of 5 engineers. How would you prioritize?",
            "category": "execution",
        },
        {
            "id": "ex_2",
            "text": "How do you measure success for a new feature launch?",
            "category": "execution",
        },
    ],
    "analytical": [
        {
            "id": "an_1",
            "text": "Estimate the market size for productivity apps in the US.",
            "category": "analytical",
        },
        {
            "id": "an_2",
            "text": "How would you estimate the total number of active users on Twitter?",
            "category": "analytical",
        },
    ],
}


def _ctx(request: Request, **kwargs) -> dict:
    """Build template context."""
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


@router.get("/tools/interview-coach", response_class=HTMLResponse)
async def interview_coach_home(request: Request) -> HTMLResponse:
    """Interview coach landing page."""
    categories = [
        {
            "id": "product_design",
            "label": "Product Design",
            "count": len(INTERVIEW_QUESTIONS.get("product_design", [])),
        },
        {
            "id": "strategy",
            "label": "Strategy",
            "count": len(INTERVIEW_QUESTIONS.get("strategy", [])),
        },
        {
            "id": "execution",
            "label": "Execution",
            "count": len(INTERVIEW_QUESTIONS.get("execution", [])),
        },
        {
            "id": "analytical",
            "label": "Analytical",
            "count": len(INTERVIEW_QUESTIONS.get("analytical", [])),
        },
    ]

    return templates.TemplateResponse(
        "interview-coach/index.html",
        _ctx(
            request,
            title="PM Interview Coach",
            current_page="/tools/interview-coach",
            categories=categories,
        ),
    )


@router.get("/tools/interview-coach/{category}", response_class=HTMLResponse)
async def interview_coach_practice(request: Request, category: str) -> HTMLResponse:
    """Practice page for a category."""
    questions = INTERVIEW_QUESTIONS.get(category, [])
    if not questions:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Category not found", current_page=""),
            status_code=404,
        )

    # Get random question
    import random

    question = random.choice(questions)
    session_id = str(uuid.uuid4())

    # Create session in database
    db = SessionLocal()
    session = InterviewSession(session_id=session_id, category=category)
    db.add(session)
    db.commit()
    db.refresh(session)
    db.close()

    return templates.TemplateResponse(
        "interview-coach/practice.html",
        _ctx(
            request,
            title=f"Practice {category}",
            current_page="/tools/interview-coach",
            question=question,
            session_id=session_id,
            category=category,
        ),
    )


@router.post("/api/interview-coach/submit", response_class=HTMLResponse)
async def submit_interview_answer(request: Request) -> HTMLResponse:
    """Submit an interview answer for evaluation."""
    form_data = await request.form()
    session_id = form_data.get("session_id")
    question_id = form_data.get("question_id")
    answer_text = form_data.get("answer_text")
    time_spent_sec = form_data.get("time_spent_sec")
    category = form_data.get("category")

    if not all([session_id, question_id, answer_text, category]):
        return "<div>Error: Missing required fields</div>"

    try:
        time_spent = int(time_spent_sec) if time_spent_sec else None
    except (ValueError, TypeError):
        time_spent = None

    try:
        # Get the question
        question = None
        for q in INTERVIEW_QUESTIONS.get(category, []):
            if q["id"] == question_id:
                question = q
                break

        if not question:
            return "<div>Error: Question not found</div>"

        # Evaluate answer
        result = await evaluate_interview_answer(
            category=category, question=question["text"], answer=answer_text, time_spent_sec=time_spent
        )

        # Save attempt to database
        db = SessionLocal()
        attempt = InterviewAttempt(
            session_id=session_id,
            question_id=question_id,
            answer_text=answer_text,
            overall_score=result.overall_score,
            framework_score=result.framework_score,
            structure_score=result.structure_score,
            completeness_score=result.completeness_score,
            strengths=json.dumps(result.strengths),
            improvements=json.dumps(result.improvements),
            suggested_framework=result.suggested_framework,
            time_spent_sec=time_spent,
        )
        db.add(attempt)
        db.commit()
        db.close()

        # Return feedback HTML
        return templates.TemplateResponse(
            "interview-coach/partials/feedback.html",
            {
                "request": request,
                "result": result,
                "answer_text": answer_text,
            },
        )

    except Exception as e:
        return f"<div class='text-danger'>Error evaluating answer: {str(e)}</div>"
