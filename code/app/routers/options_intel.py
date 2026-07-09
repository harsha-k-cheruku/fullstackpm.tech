"""Webhook receiver and dashboard for the Daily Options Intelligence System."""
from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.options_intel import OptionsIntelNotification

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

MAX_PAYLOAD_BYTES = 256_000


# ── Auth ──────────────────────────────────────────────────────────────────────

def require_options_intel_token(x_options_intel_token: Optional[str] = Header(default=None)) -> None:
    expected = settings.options_intel_webhook_token
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Options Intel webhook token is not configured",
        )
    if not x_options_intel_token or x_options_intel_token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook token")


# ── Webhook receiver ──────────────────────────────────────────────────────────

@router.post("/api/options-intel/notify", tags=["options-intel"])
async def capture_notification(
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_options_intel_token),
):
    """Capture one Options Intel notification payload."""
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Payload is required")
    if len(body) > MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Payload too large")

    content_type = request.headers.get("content-type", "")
    payload_text = _normalize_payload(body, content_type)
    event_type = _event_type(payload_text)

    row = OptionsIntelNotification(
        event_type=event_type,
        content_type=content_type,
        source_ip=request.client.host if request.client else None,
        payload_text=payload_text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {"ok": True, "id": row.id, "event_type": row.event_type, "created_at": row.created_at.isoformat()}


@router.get("/api/options-intel/notifications/latest", tags=["options-intel"])
async def latest_notification(
    db: Session = Depends(get_db),
    _: None = Depends(require_options_intel_token),
):
    """Return the latest captured notification (debugging)."""
    row = db.query(OptionsIntelNotification).order_by(OptionsIntelNotification.created_at.desc()).first()
    if row is None:
        raise HTTPException(status_code=404, detail="No notifications captured yet")
    return row.to_dict()


# ── Dashboard page ────────────────────────────────────────────────────────────

@router.get("/options-intel", response_class=HTMLResponse)
async def options_intel_dashboard(request: Request, db: Session = Depends(get_db)):
    """Public dashboard showing the latest morning brief and run history."""
    rows = (
        db.query(OptionsIntelNotification)
        .order_by(OptionsIntelNotification.created_at.desc())
        .limit(30)
        .all()
    )

    latest = None
    history = []
    for i, row in enumerate(rows):
        parsed = _parse_brief(row.payload_text, row.created_at)
        if i == 0:
            latest = parsed
        history.append(_brief_summary(parsed))

    return templates.TemplateResponse(
        "options_intel.html",
        {
            "request": request,
            "config": settings,
            "year": datetime.now().year,
            "title": "Options Intel — fullstackpm.tech",
            "meta_description": "Daily pre-market regime analysis and options trade signals for SPY, NVDA, and AMZN.",
            "current_page": "/options-intel",
            "latest": latest,
            "history": history,
        },
    )


# ── Brief parser ──────────────────────────────────────────────────────────────

def _parse_brief(payload_text: str, created_at: datetime | None = None) -> dict[str, Any]:
    """Parse a stored JSON payload into structured brief fields."""
    try:
        payload = json.loads(payload_text)
        body: str = payload.get("body", "")
    except (json.JSONDecodeError, AttributeError):
        return {"raw": payload_text, "parse_error": True, "tickers": [], "created_at": created_at}

    lines = body.strip().split("\n")
    result: dict[str, Any] = {
        "raw": body,
        "date": None,
        "snapshot_id": None,
        "vix": None,
        "hy_oas": None,
        "breadth": None,
        "tickers": [],
        "discipline": None,
        "data_quality": None,
        "portfolio_risk": None,
        "parse_error": False,
        "created_at": created_at,
    }

    for line in lines:
        if line.startswith("MORNING INTEL"):
            m = re.match(r"MORNING INTEL — (\S+) \(snapshot (\S+)\)", line)
            if m:
                result["date"] = m.group(1)
                result["snapshot_id"] = m.group(2)

        elif line.startswith("Regime data:"):
            m = re.search(r"VIX ([\d.]+)", line)
            if m:
                result["vix"] = m.group(1)
            m = re.search(r"HY OAS ([\d.]+)", line)
            if m:
                result["hy_oas"] = m.group(1)
            m = re.search(r"Breadth ([\d.]+)%", line)
            if m:
                result["breadth"] = m.group(1)

        elif re.match(r"^(SPY|NVDA|AMZN):", line):
            ticker = line.split(":")[0]
            rest = line[len(ticker) + 1:].strip()
            if "NO_TRADE" in rest:
                detail = rest.split(" — ", 1)[1] if " — " in rest else rest
                result["tickers"].append({"ticker": ticker, "status": "NO_TRADE", "detail": detail})
            elif "TRADE" in rest and "|" in rest:
                result["tickers"].append({"ticker": ticker, "status": "TRADE", "detail": rest})
            else:
                result["tickers"].append({"ticker": ticker, "status": "UNKNOWN", "detail": rest})

        elif line.startswith("Discipline:"):
            result["discipline"] = line[len("Discipline:"):].strip()

        elif line.startswith("Data quality:"):
            result["data_quality"] = line[len("Data quality:"):].strip()

        elif line.startswith("Portfolio risk"):
            result["portfolio_risk"] = line.split(":", 1)[1].strip() if ":" in line else line

    return result


def _brief_summary(parsed: dict[str, Any]) -> dict[str, Any]:
    """Compact row for the history table."""
    return {
        "date": parsed.get("date"),
        "created_at": parsed.get("created_at"),
        "vix": parsed.get("vix"),
        "data_quality": parsed.get("data_quality"),
        "tickers": [
            {"ticker": t["ticker"], "status": t["status"]}
            for t in parsed.get("tickers", [])
        ],
        "has_trade": any(t["status"] == "TRADE" for t in parsed.get("tickers", [])),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _normalize_payload(body: bytes, content_type: str) -> str:
    text = body.decode("utf-8", errors="replace")
    if "application/json" not in content_type.lower():
        return text
    try:
        parsed: Any = json.loads(text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from None
    return json.dumps(parsed, sort_keys=True, separators=(",", ":"))


def _event_type(payload_text: str) -> str:
    try:
        parsed = json.loads(payload_text)
    except json.JSONDecodeError:
        return "notification"
    if isinstance(parsed, dict):
        value = parsed.get("event_type") or parsed.get("type") or parsed.get("title")
        if isinstance(value, str) and value.strip():
            return value.strip()[:80]
    return "notification"
