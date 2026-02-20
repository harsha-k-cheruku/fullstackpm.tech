# app/routers/sde_prep.py
"""SDE prep tracker routes and APIs."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.sde_prep import (
    BehavioralStory,
    DailyLog,
    DailyTask,
    DifficultyEnum,
    LeetCodeProblem,
    PracticeSession,
    ProblemCategoryEnum,
    ProblemStatusEnum,
    SystemDesignStatusEnum,
    SystemDesignTopic,
    WeekPlan,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def get_current_user_id(request: Request) -> Optional[int]:
    """Get user_id from session cookie."""
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(user_id)


def _ctx(request: Request, **kwargs) -> dict:
    """Build default template context."""
    return {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        **kwargs,
    }


def _parse_enum(value: Optional[str], enum_cls: type) -> Any:
    if not value or value == "all":
        return None
    try:
        return enum_cls[value]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Invalid filter value") from exc


def _bool_value(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"true", "1", "yes", "on"}
    return None


async def _read_payload(request: Request) -> Dict[str, Any]:
    if request.headers.get("content-type", "").startswith("application/json"):
        return await request.json()
    form = await request.form()
    return dict(form)


@router.get("/tools/sde-prep", response_class=HTMLResponse)
async def landing(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/landing.html",
        _ctx(request, title="SDE Prep Tracker", current_page=""),
    )


@router.get("/tools/sde-prep/prfaq", response_class=HTMLResponse)
async def prfaq(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/prfaq.html",
        _ctx(request, title="SDE Prep Tracker — About & FAQ", current_page="/tools/sde-prep/prfaq"),
    )


@router.get("/tools/sde-prep/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/dashboard.html",
        _ctx(request, title="SDE Prep Tracker — Dashboard", current_page=""),
    )


@router.get("/tools/sde-prep/problems", response_class=HTMLResponse)
async def problems(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/problems.html",
        _ctx(
            request,
            title="LeetCode Problems — SDE Prep",
            current_page="",
            categories=[c.value for c in ProblemCategoryEnum],
            difficulties=[d.value for d in DifficultyEnum],
            statuses=[s.value for s in ProblemStatusEnum],
        ),
    )


@router.get("/tools/sde-prep/daily-plan", response_class=HTMLResponse)
async def daily_plan(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/daily_plan.html",
        _ctx(request, title="Daily Plan — SDE Prep", current_page=""),
    )


@router.get("/tools/sde-prep/weekly-plan", response_class=HTMLResponse)
async def weekly_plan(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/weekly_plan.html",
        _ctx(request, title="Weekly Plan — SDE Prep", current_page=""),
    )


@router.get("/tools/sde-prep/system-design", response_class=HTMLResponse)
async def system_design(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "sde-prep/system_design.html",
        _ctx(request, title="System Design — SDE Prep", current_page=""),
    )


@router.get("/tools/sde-prep/behavioral", response_class=HTMLResponse)
async def behavioral(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user_id = get_current_user_id(request)
    stories = (
        db.query(BehavioralStory)
        .filter_by(user_id=user_id)
        .order_by(BehavioralStory.id.desc())
        .all()
    )
    return templates.TemplateResponse(
        "sde-prep/behavioral.html",
        _ctx(
            request,
            title="Behavioral Stories — SDE Prep",
            current_page="",
            stories=stories,
        ),
    )


@router.get("/tools/sde-prep/study-plan", response_class=HTMLResponse)
async def study_plan(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user_id = get_current_user_id(request)
    weeks = (
        db.query(WeekPlan)
        .filter_by(user_id=user_id)
        .order_by(WeekPlan.week_number)
        .all()
    )
    return templates.TemplateResponse(
        "sde-prep/study_plan.html",
        _ctx(
            request,
            title="Study Plan — SDE Prep",
            current_page="",
            weeks=weeks,
        ),
    )


@router.get("/api/sde-prep/dashboard/stats")
async def dashboard_stats(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    user_id = get_current_user_id(request)
    total = db.query(LeetCodeProblem).filter_by(user_id=user_id).count()
    solved = (
        db.query(LeetCodeProblem)
        .filter_by(user_id=user_id)
        .filter(LeetCodeProblem.status == ProblemStatusEnum.COMPLETED)
        .count()
    )
    blind_75 = (
        db.query(LeetCodeProblem)
        .filter_by(user_id=user_id)
        .filter(LeetCodeProblem.is_blind_75.is_(True))
        .count()
    )

    def _count_difficulty(level: DifficultyEnum) -> int:
        return (
            db.query(LeetCodeProblem)
            .filter_by(user_id=user_id)
            .filter(LeetCodeProblem.difficulty == level)
            .count()
        )

    by_difficulty = {
        "EASY": _count_difficulty(DifficultyEnum.EASY),
        "MEDIUM": _count_difficulty(DifficultyEnum.MEDIUM),
        "HARD": _count_difficulty(DifficultyEnum.HARD),
    }

    topic_total = db.query(SystemDesignTopic).filter_by(user_id=user_id).count()
    topic_confident = (
        db.query(SystemDesignTopic)
        .filter_by(user_id=user_id)
        .filter(SystemDesignTopic.status == SystemDesignStatusEnum.CONFIDENT)
        .count()
    )

    stories_total = db.query(BehavioralStory).filter_by(user_id=user_id).count()
    stories_ready = (
        db.query(BehavioralStory)
        .filter_by(user_id=user_id)
        .filter(BehavioralStory.is_ready.is_(True))
        .count()
    )

    week = (
        db.query(WeekPlan)
        .filter_by(user_id=user_id)
        .filter(WeekPlan.is_completed.is_(False))
        .order_by(WeekPlan.week_number)
        .first()
        or db.query(WeekPlan)
        .filter_by(user_id=user_id)
        .order_by(WeekPlan.week_number.desc())
        .first()
    )

    weekly_progress = [
        {"week": w.week_number, "percentage": w.completion_percentage}
        for w in db.query(WeekPlan)
        .filter_by(user_id=user_id)
        .order_by(WeekPlan.week_number)
        .all()
    ]

    logs = db.query(DailyLog).filter_by(user_id=user_id).order_by(DailyLog.date.desc()).all()
    streak = 0
    expected = date.today()
    for log in logs:
        if log.date == expected:
            streak += 1
            expected = expected - timedelta(days=1)
        else:
            break

    days = [date.today() - timedelta(days=i) for i in range(14)][::-1]
    hours_map = {log.date: log.study_hours for log in logs}
    study_hours = [hours_map.get(day, 0) for day in days]

    return JSONResponse(
        {
            "leetcode": {
                "solved": solved,
                "total": total,
                "percentage": round((solved / total * 100) if total else 0, 1),
                "blind_75_count": blind_75,
                "by_difficulty": by_difficulty,
            },
            "system_design": {
                "confident": topic_confident,
                "total": topic_total,
                "percentage": round((topic_confident / topic_total * 100) if topic_total else 0, 1),
            },
            "behavioral": {
                "ready": stories_ready,
                "total": stories_total,
                "percentage": round((stories_ready / stories_total * 100) if stories_total else 0, 1),
            },
            "current_week": {
                "title": week.title if week else "",
                "percentage": week.completion_percentage if week else 0,
            },
            "streak_days": streak,
            "charts_data": {
                "difficulty": by_difficulty,
                "weekly_progress": weekly_progress,
                "study_hours": {
                    "labels": [day.strftime("%b %d") for day in days],
                    "values": study_hours,
                },
            },
        }
    )


@router.get("/api/sde-prep/problems", response_class=HTMLResponse)
async def problems_table(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user_id = get_current_user_id(request)
    category = _parse_enum(request.query_params.get("category"), ProblemCategoryEnum)
    difficulty = _parse_enum(request.query_params.get("difficulty"), DifficultyEnum)
    status = _parse_enum(request.query_params.get("status"), ProblemStatusEnum)
    blind_75 = _bool_value(request.query_params.get("blind_75_only"))

    query = db.query(LeetCodeProblem).filter_by(user_id=user_id)
    if category:
        query = query.filter(LeetCodeProblem.category == category)
    if difficulty:
        query = query.filter(LeetCodeProblem.difficulty == difficulty)
    if status:
        query = query.filter(LeetCodeProblem.status == status)
    if blind_75:
        query = query.filter(LeetCodeProblem.is_blind_75.is_(True))

    problems = query.order_by(LeetCodeProblem.number).all()
    return templates.TemplateResponse(
        "sde-prep/partials/problems_table.html",
        _ctx(request, problems=problems),
    )


@router.put("/api/sde-prep/problems/{problem_id}")
async def update_problem(
    problem_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    problem = (
        db.query(LeetCodeProblem)
        .filter_by(user_id=user_id)
        .filter(LeetCodeProblem.id == problem_id)
        .first()
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    try:
        status_value = payload.get("status")
        if status_value:
            problem.status = ProblemStatusEnum[status_value]
            if problem.status == ProblemStatusEnum.COMPLETED:
                problem.completed_at = datetime.now()

        for field in [
            "notes",
            "solution_approach",
            "time_complexity",
            "space_complexity",
        ]:
            if field in payload:
                setattr(problem, field, payload[field])

        db.commit()
        db.refresh(problem)
        return JSONResponse(problem.to_dict())
    except (KeyError, SQLAlchemyError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid payload") from exc


@router.post("/api/sde-prep/problems/{problem_id}/practice")
async def add_practice_session(
    problem_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    problem = (
        db.query(LeetCodeProblem)
        .filter_by(user_id=user_id)
        .filter(LeetCodeProblem.id == problem_id)
        .first()
    )
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    try:
        session = PracticeSession(
            problem_id=problem.id,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            time_taken_minutes=int(payload.get("time_taken_minutes") or 0),
            solved_on_own=_bool_value(payload.get("solved_on_own")) or False,
            needed_hints=_bool_value(payload.get("needed_hints")) or False,
            notes=payload.get("notes"),
            user_id=user_id,
        )
        problem.attempts += 1
        if session.solved_on_own:
            problem.status = ProblemStatusEnum.COMPLETED
            problem.completed_at = datetime.now()
            problem.time_taken_minutes = session.time_taken_minutes
        db.add(session)
        db.commit()
        return JSONResponse({"status": "ok", "practice_id": session.id})
    except (ValueError, SQLAlchemyError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid payload") from exc


@router.get("/api/sde-prep/daily-tasks", response_class=HTMLResponse)
async def daily_tasks(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user_id = get_current_user_id(request)
    week_number = request.query_params.get("week")
    day_number = request.query_params.get("day")
    if not week_number:
        return templates.TemplateResponse(
            "sde-prep/partials/daily_tasks.html",
            _ctx(
                request,
                tasks=[],
                week_number=None,
                day_name="",
                task_count=0,
                total_minutes=0,
                completion_percentage=0,
                selected_day=0,
            ),
        )

    week_number_int = int(week_number)
    day_number_int = int(day_number or 0)

    query = (
        db.query(DailyTask)
        .filter_by(user_id=user_id)
        .filter(DailyTask.week_number == week_number_int)
    )
    if day_number_int:
        query = query.filter(DailyTask.day_number == day_number_int)
    tasks = query.order_by(DailyTask.day_number, DailyTask.task_order).all()

    task_count = len(tasks)
    completed_count = len([task for task in tasks if task.is_completed])
    total_minutes = sum(task.estimated_minutes or 0 for task in tasks)
    completion_percentage = round(
        (completed_count / task_count * 100) if task_count else 0, 1
    )

    day_name = "All Days" if day_number_int == 0 else (tasks[0].day_name if tasks else "")

    return templates.TemplateResponse(
        "sde-prep/partials/daily_tasks.html",
        _ctx(
            request,
            tasks=tasks,
            week_number=week_number_int,
            day_name=day_name,
            task_count=task_count,
            total_minutes=total_minutes,
            completion_percentage=completion_percentage,
            selected_day=day_number_int,
        ),
    )


@router.put("/api/sde-prep/daily-tasks/{task_id}")
async def update_daily_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    task = (
        db.query(DailyTask)
        .filter_by(user_id=user_id)
        .filter(DailyTask.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        if "is_completed" in payload:
            is_completed = _bool_value(payload.get("is_completed")) or False
            task.is_completed = is_completed
            task.completed_at = datetime.now() if is_completed else None
        if "notes" in payload:
            task.notes = payload.get("notes")

        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Update failed") from exc

    selected_week = int(payload.get("week") or task.week_number)
    selected_day = int(payload.get("day") or task.day_number)
    query_string = f"week={selected_week}&day={selected_day}".encode()
    new_scope = {**request.scope, "query_string": query_string}
    return await daily_tasks(Request(new_scope), db)


@router.get("/api/sde-prep/system-design", response_class=HTMLResponse)
async def system_design_topics(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    user_id = get_current_user_id(request)
    topics = (
        db.query(SystemDesignTopic)
        .filter_by(user_id=user_id)
        .order_by(SystemDesignTopic.title)
        .all()
    )
    return templates.TemplateResponse(
        "sde-prep/partials/system_design_cards.html",
        _ctx(request, topics=topics, statuses=[s.value for s in SystemDesignStatusEnum]),
    )


@router.put("/api/sde-prep/system-design/{topic_id}")
async def update_system_design_topic(
    topic_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    topic = (
        db.query(SystemDesignTopic)
        .filter_by(user_id=user_id)
        .filter(SystemDesignTopic.id == topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    try:
        if "status" in payload and payload["status"]:
            topic.status = SystemDesignStatusEnum[payload["status"]]
        for field in ["notes", "key_concepts", "common_patterns"]:
            if field in payload:
                setattr(topic, field, payload[field])
        if "practice_count" in payload:
            topic.practice_count = int(payload["practice_count"])
            topic.last_practiced = datetime.now()
        db.commit()
        db.refresh(topic)
        return JSONResponse(topic.to_dict())
    except (KeyError, SQLAlchemyError, ValueError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid payload") from exc


@router.get("/api/sde-prep/behavioral")
async def list_behavioral(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    user_id = get_current_user_id(request)
    stories = (
        db.query(BehavioralStory)
        .filter_by(user_id=user_id)
        .order_by(BehavioralStory.id.desc())
        .all()
    )
    return JSONResponse([story.to_dict() for story in stories])


@router.post("/api/sde-prep/behavioral")
async def create_behavioral(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    try:
        story = BehavioralStory(
            title=payload.get("title", "Untitled Story"),
            category=payload.get("category", "General"),
            situation=payload.get("situation"),
            task=payload.get("task"),
            action=payload.get("action"),
            result=payload.get("result"),
            company_relevance=payload.get("company_relevance"),
            leadership_principle=payload.get("leadership_principle"),
            notes=payload.get("notes"),
            user_id=user_id,
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return JSONResponse(story.to_dict())
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="Create failed") from exc


@router.put("/api/sde-prep/behavioral/{story_id}")
async def update_behavioral(
    story_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    story = (
        db.query(BehavioralStory)
        .filter_by(user_id=user_id)
        .filter(BehavioralStory.id == story_id)
        .first()
    )
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    try:
        for field in [
            "title",
            "category",
            "situation",
            "task",
            "action",
            "result",
            "company_relevance",
            "leadership_principle",
            "notes",
        ]:
            if field in payload:
                setattr(story, field, payload[field])
        if "times_practiced" in payload:
            story.times_practiced = int(payload["times_practiced"])
            story.last_practiced = datetime.now()
        if "is_ready" in payload:
            story.is_ready = _bool_value(payload["is_ready"]) or False
        db.commit()
        db.refresh(story)
        return JSONResponse(story.to_dict())
    except (ValueError, SQLAlchemyError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed") from exc


@router.get("/api/sde-prep/weeks")
async def list_weeks(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    user_id = get_current_user_id(request)
    weeks = (
        db.query(WeekPlan)
        .filter_by(user_id=user_id)
        .order_by(WeekPlan.week_number)
        .all()
    )
    return JSONResponse([week.to_dict() for week in weeks])


@router.put("/api/sde-prep/weeks/{week_id}")
async def update_week(
    week_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> JSONResponse:
    user_id = get_current_user_id(request)
    payload = await _read_payload(request)
    week = (
        db.query(WeekPlan)
        .filter_by(user_id=user_id)
        .filter(WeekPlan.id == week_id)
        .first()
    )
    if not week:
        raise HTTPException(status_code=404, detail="Week not found")

    try:
        if "is_completed" in payload:
            week.is_completed = _bool_value(payload["is_completed"]) or False
        if "completion_percentage" in payload:
            week.completion_percentage = float(payload["completion_percentage"])
        if "notes" in payload:
            week.notes = payload.get("notes")
        db.commit()
        db.refresh(week)
        return JSONResponse(week.to_dict())
    except (ValueError, SQLAlchemyError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed") from exc
