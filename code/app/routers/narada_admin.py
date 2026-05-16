from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.narada_override import NaradaOverride

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


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


# ── Admin UI ──────────────────────────────────────────────────────────────────

@router.get("/admin/narada", response_class=HTMLResponse)
async def narada_admin_page(request: Request, db: Session = Depends(get_db)):
    morning = _get_or_create(db, "morning")
    return templates.TemplateResponse("admin/narada_config.html", {
        "request": request,
        "config": settings,
        "year": datetime.now().year,
        "title": "Narada Admin",
        "morning": morning,
        "saved": request.query_params.get("saved"),
        "error": request.query_params.get("error"),
    })


@router.post("/admin/narada/save")
async def narada_admin_save(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    password = str(form.get("password", ""))

    if not _check_admin_password(password):
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/admin/narada?error=wrong_password", status_code=303)

    pipeline = str(form.get("pipeline", "morning"))
    row = _get_or_create(db, pipeline)

    row.global_news_enabled = form.get("global_news_enabled") == "on"
    row.spy_learning_enabled = form.get("spy_learning_enabled") == "on"
    row.market_brief_enabled = form.get("market_brief_enabled") == "on"
    row.analytics_pm_enabled = form.get("analytics_pm_enabled") == "on"

    row.notes_general = str(form.get("notes_general", "")).strip()
    row.notes_news    = str(form.get("notes_news", "")).strip()
    row.notes_spy     = str(form.get("notes_spy", "")).strip()
    row.notes_market  = str(form.get("notes_market", "")).strip()
    row.notes_pm      = str(form.get("notes_pm", "")).strip()

    row.updated_at = datetime.utcnow()
    db.commit()

    from fastapi.responses import RedirectResponse
    return RedirectResponse("/admin/narada?saved=1", status_code=303)


# ── Pipeline API (Mac mini pulls this before each run) ────────────────────────

@router.get("/api/narada/config")
async def narada_config_api(request: Request, db: Session = Depends(get_db)):
    if not _check_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized")

    pipeline = request.query_params.get("pipeline", "morning")
    row = _get_or_create(db, pipeline)

    return JSONResponse({
        "pipeline": row.pipeline,
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
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    })
