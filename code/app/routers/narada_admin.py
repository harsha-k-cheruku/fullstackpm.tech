from __future__ import annotations

import os
import yaml
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.narada_override import NaradaOverride

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

BACKSTORY_CURRICULUM = Path("/Users/sidc/Projects/claude_code/project_narada/curriculum/backstory_curriculum.yaml")
SPY_CURRICULUM = Path("/Users/sidc/Projects/claude_code/project_narada/curriculum/spy_curriculum.yaml")


def _get_or_create(db: Session, pipeline: str) -> NaradaOverride:
    row = db.query(NaradaOverride).filter_by(pipeline=pipeline).first()
    if not row:
        row = NaradaOverride(pipeline=pipeline)
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def _check_admin_password(password: str) -> bool:
    expected = os.getenv("NARADA_ADMIN_PASSWORD", "")
    return bool(expected and password == expected)


def _check_api_key(request: Request) -> bool:
    expected = os.getenv("NARADA_API_KEY", "")
    auth = request.headers.get("Authorization", "")
    return bool(expected and auth == f"Bearer {expected}")


def _next_backstory() -> dict:
    """Return the next backstory episode from the curriculum."""
    try:
        data = yaml.safe_load(BACKSTORY_CURRICULUM.read_text()) or {}
        episodes = data.get("episodes", [])
        idx = int(data.get("current_index", 0)) % max(len(episodes), 1)
        ep = episodes[idx] if episodes else {}
        return {
            "index": idx,
            "total": len(episodes),
            "id": ep.get("id", ""),
            "title": ep.get("title", "—"),
            "hook": ep.get("hook", ""),
            "theme": ep.get("theme", ""),
            "era": ep.get("era", ""),
        }
    except Exception:
        return {"index": 0, "total": 0, "title": "—", "hook": "", "theme": "", "era": ""}


def _next_spy_lesson() -> dict:
    """Return the next SPY curriculum lesson."""
    try:
        data = yaml.safe_load(SPY_CURRICULUM.read_text()) or {}
        week = int(data.get("current_week", 1))
        day = int(data.get("current_day", 1))
        weeks = data.get("weeks", {})
        week_data = weeks.get(week) or weeks.get(str(week)) or {}
        days = week_data.get("days", {})
        lesson = days.get(day) or days.get(str(day)) or "—"
        return {"week": week, "day": day, "topic": week_data.get("topic", ""), "lesson": lesson}
    except Exception:
        return {"week": 1, "day": 1, "topic": "", "lesson": "—"}


# ── Admin UI ──────────────────────────────────────────────────────────────────

def _pipe_segments(tab: str, row: NaradaOverride) -> list:
    if tab == "morning":
        return [
            ("global_news_enabled",  "Global News Roundup", row.global_news_enabled),
            ("spy_learning_enabled", "SPY Learning",         row.spy_learning_enabled),
            ("market_brief_enabled", "Market Brief",         row.market_brief_enabled),
            ("analytics_pm_enabled", "PM / Analytics",       row.analytics_pm_enabled),
        ]
    return [
        ("global_news_enabled",  "AI News",    row.global_news_enabled),
        ("spy_learning_enabled", "PM News",    row.spy_learning_enabled),
        ("market_brief_enabled", "PM Learning",row.market_brief_enabled),
    ]


def _pipe_notes(tab: str, row: NaradaOverride) -> list:
    if tab == "morning":
        return [
            ("notes_general", "General / Today's Focus", row.notes_general, "e.g. Big FOMC day, watch 4:30 PM"),
            ("notes_news",    "Global News",              row.notes_news,    "e.g. Focus on US-China trade"),
            ("notes_spy",     "SPY / Options",            row.notes_spy,     "e.g. IV spike — explain gamma risk"),
            ("notes_market",  "Market Brief",             row.notes_market,  "e.g. Watch XLF — financials leading"),
            ("notes_pm",      "PM / Analytics",           row.notes_pm,      "e.g. Focus on discovery frameworks"),
        ]
    return [
        ("notes_general", "General Focus", row.notes_general, "e.g. Prioritise practical PM tools today"),
        ("notes_news",    "AI News",       row.notes_news,    "e.g. Focus on model releases, skip research papers"),
        ("notes_spy",     "PM News",       row.notes_spy,     "e.g. Prioritise Lenny or Shreyas if available"),
        ("notes_market",  "PM Learning",   row.notes_market,  "e.g. Cover discovery — no metrics posts today"),
        ("notes_pm",      "Skip / Avoid",  row.notes_pm,      "e.g. Skip engineering-heavy posts"),
    ]


@router.get("/admin/narada", response_class=HTMLResponse)
async def narada_admin_page(request: Request, db: Session = Depends(get_db)):
    tab = request.query_params.get("tab", "morning")
    morning = _get_or_create(db, "morning")
    afternoon = _get_or_create(db, "afternoon")
    weekend = _get_or_create(db, "weekend")
    pipe_row = morning if tab == "morning" else afternoon

    return templates.TemplateResponse("admin/narada_config.html", {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        "title": "Narada Admin",
        "tab": tab,
        "morning": morning,
        "afternoon": afternoon,
        "weekend": weekend,
        "pipe_row": pipe_row,
        "pipe_segments": _pipe_segments(tab, pipe_row),
        "pipe_notes": _pipe_notes(tab, pipe_row),
        "next_backstory": _next_backstory(),
        "next_spy": _next_spy_lesson(),
        "saved": request.query_params.get("saved"),
        "error": request.query_params.get("error"),
    })


@router.post("/admin/narada/save")
async def narada_admin_save(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    password = str(form.get("password", ""))

    if not _check_admin_password(password):
        return RedirectResponse("/admin/narada?error=wrong_password", status_code=303)

    pipeline = str(form.get("pipeline", "morning"))
    row = _get_or_create(db, pipeline)

    if pipeline in ("morning", "afternoon"):
        row.global_news_enabled  = form.get("global_news_enabled") == "on"
        row.spy_learning_enabled = form.get("spy_learning_enabled") == "on"
        row.market_brief_enabled = form.get("market_brief_enabled") == "on"
        row.analytics_pm_enabled = form.get("analytics_pm_enabled") == "on"
        row.notes_general = str(form.get("notes_general", "")).strip()
        row.notes_news    = str(form.get("notes_news", "")).strip()
        row.notes_spy     = str(form.get("notes_spy", "")).strip()
        row.notes_market  = str(form.get("notes_market", "")).strip()
        row.notes_pm      = str(form.get("notes_pm", "")).strip()
        row.source_url    = str(form.get("source_url", "")).strip()

    if pipeline == "weekend":
        row.topic_override = str(form.get("topic_override", "")).strip()
        row.url_override   = str(form.get("url_override", "")).strip()

    row.updated_at = datetime.utcnow()
    db.commit()

    return RedirectResponse(f"/admin/narada?saved=1&tab={pipeline}", status_code=303)


# ── Pipeline API (Mac mini pulls this before each run) ────────────────────────

@router.get("/api/narada/config")
async def narada_config_api(request: Request, db: Session = Depends(get_db)):
    if not _check_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized")

    pipeline = request.query_params.get("pipeline", "morning")
    row = _get_or_create(db, pipeline)

    base = {
        "pipeline": row.pipeline,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }

    if pipeline in ("morning", "afternoon"):
        base.update({
            "segments": {
                "global_news":  {"enabled": row.global_news_enabled},
                "spy_learning": {"enabled": row.spy_learning_enabled},
                "market_brief": {"enabled": row.market_brief_enabled},
                "analytics_pm": {"enabled": row.analytics_pm_enabled},
            },
            "notes": {
                "general":      row.notes_general or "",
                "news":         row.notes_news or "",
                "spy_options":  row.notes_spy or "",
                "today_focus":  row.notes_market or "",
                "pm_analytics": row.notes_pm or "",
            },
            "source_url": row.source_url or "",
        })

    if pipeline == "weekend":
        base.update({
            "topic_override": row.topic_override or "",
            "url_override":   row.url_override or "",
        })

    return JSONResponse(base)


@router.post("/api/narada/clear-source-url")
async def narada_clear_source_url(request: Request, db: Session = Depends(get_db)):
    """Called by the pipeline after successfully consuming source_url."""
    if not _check_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    pipeline = request.query_params.get("pipeline", "morning")
    row = _get_or_create(db, pipeline)
    row.source_url = ""
    row.updated_at = datetime.utcnow()
    db.commit()
    return JSONResponse({"cleared": True})
