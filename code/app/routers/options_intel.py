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
    """Parse a stored JSON payload. Uses structured field when present, falls back to body text."""
    try:
        payload = json.loads(payload_text)
    except (json.JSONDecodeError, AttributeError):
        return {"raw": payload_text, "parse_error": True, "tickers": [], "news": [], "created_at": created_at}

    body: str = payload.get("body", "")
    structured: dict | None = payload.get("structured")

    # Base result from text parsing (always available as fallback)
    result: dict[str, Any] = {
        "raw": body,
        "date": None,
        "snapshot_id": None,
        "vix": None,
        "hy_oas": None,
        "breadth": None,
        "tickers": [],
        "news": [],
        "takeaway": None,
        "regime": None,
        "discipline": None,
        "data_quality": None,
        "warmup_days_remaining": None,
        "parse_error": False,
        "created_at": created_at,
    }

    # Text-based fallback parsing
    for line in body.strip().split("\n"):
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
                result["tickers"].append({"ticker": ticker, "status": "NO_TRADE", "detail": detail,
                                          "spot": None, "iv_30d_pct": None, "sentiment_score": None,
                                          "sentiment_driver": None, "bias": None, "range_low": None,
                                          "range_high": None, "strategy": None, "contracts": 0})
            elif "TRADE" in rest:
                result["tickers"].append({"ticker": ticker, "status": "TRADE", "detail": rest,
                                          "spot": None, "iv_30d_pct": None, "sentiment_score": None,
                                          "sentiment_driver": None, "bias": None, "range_low": None,
                                          "range_high": None, "strategy": None, "contracts": 0})
        elif line.startswith("Discipline:"):
            result["discipline"] = line[len("Discipline:"):].strip()
        elif line.startswith("Data quality:"):
            result["data_quality"] = line[len("Data quality:"):].strip()

    # Overlay with structured data when available (much richer)
    if structured:
        result["date"] = structured.get("date") or result["date"]
        result["snapshot_id"] = structured.get("snapshot_id") or result["snapshot_id"]
        result["takeaway"] = structured.get("takeaway")
        result["warmup_days_remaining"] = structured.get("warmup_days_remaining")
        result["regime"] = structured.get("regime")
        result["news"] = structured.get("news", [])

        if result["regime"]:
            result["vix"] = str(result["regime"].get("vix", ""))
            result["hy_oas"] = str(result["regime"].get("hy_oas_bps", ""))
            result["breadth"] = str(result["regime"].get("breadth_pct", ""))

        tickers_data = structured.get("tickers", {})
        result["tickers"] = []
        for t_name in ("SPY", "NVDA", "AMZN"):
            t = tickers_data.get(t_name, {})
            result["tickers"].append({
                "ticker": t_name,
                "status": "TRADE" if t.get("contracts", 0) > 0 else "NO_TRADE",
                "detail": t.get("gate_failure_detail") or t.get("gate_failure") or "",
                "spot": t.get("spot"),
                "iv_30d_pct": t.get("iv_30d_pct"),
                "iv_rank": t.get("iv_rank"),
                "sentiment_score": t.get("sentiment_score"),
                "sentiment_driver": t.get("sentiment_driver"),
                "gate_failure": t.get("gate_failure"),
                "bias": t.get("bias"),
                "confidence_pct": t.get("confidence_pct"),
                "range_low": t.get("range_low"),
                "range_high": t.get("range_high"),
                "strategy": t.get("strategy"),
                "contracts": t.get("contracts", 0),
                "conviction": t.get("conviction"),
            })

    return result


def _brief_summary(parsed: dict[str, Any]) -> dict[str, Any]:
    """Compact row for the history table."""
    return {
        "date": parsed.get("date"),
        "created_at": parsed.get("created_at"),
        "vix": parsed.get("vix"),
        "data_quality": parsed.get("data_quality"),
        "tickers": [{"ticker": t["ticker"], "status": t["status"]} for t in parsed.get("tickers", [])],
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
