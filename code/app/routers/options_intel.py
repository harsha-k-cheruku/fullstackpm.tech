"""Webhook receiver and dashboard for the Daily Options Intelligence System."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
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
LATEST_JSON = settings.data_dir / "options_intel_latest.json"
OUTCOME_JSON = settings.data_dir / "options_intel_outcome.json"


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


@router.get("/api/options-intel/status", tags=["options-intel"])
async def status(
    db: Session = Depends(get_db),
    _: None = Depends(require_options_intel_token),
):
    """Diagnostic: report what each data source has and which is being served."""
    report: dict = {"file": None, "db": None, "serving": None}

    # File source
    entry = _load_latest_json()
    if entry:
        structured = entry.get("structured", {})
        tickers = structured.get("tickers", {})
        report["file"] = {
            "written_at": entry.get("written_at"),
            "date": structured.get("date"),
            "snapshot_id": structured.get("snapshot_id"),
            "has_market_overview": bool(structured.get("market_overview")),
            "market_overview_count": len(structured.get("market_overview") or []),
            "has_looking_ahead": bool(structured.get("looking_ahead")),
            "tickers": {
                t: {
                    "iv_30d": tickers.get(t, {}).get("iv_30d_pct"),
                    "iv_rank": tickers.get(t, {}).get("iv_rank"),
                    "gate_passed": tickers.get(t, {}).get("gate_passed"),
                    "contracts": tickers.get(t, {}).get("contracts"),
                }
                for t in ("SPY", "NVDA", "AMZN")
            },
        }

    # DB source
    row = db.query(OptionsIntelNotification).order_by(OptionsIntelNotification.created_at.desc()).first()
    if row:
        try:
            payload = json.loads(row.payload_text)
            structured = payload.get("structured", {})
            tickers = structured.get("tickers", {})
            report["db"] = {
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "date": structured.get("date"),
                "snapshot_id": structured.get("snapshot_id"),
                "has_market_overview": bool(structured.get("market_overview")),
                "market_overview_count": len(structured.get("market_overview") or []),
                "has_looking_ahead": bool(structured.get("looking_ahead")),
                "tickers": {
                    t: {
                        "iv_30d": tickers.get(t, {}).get("iv_30d_pct"),
                        "iv_rank": tickers.get(t, {}).get("iv_rank"),
                        "gate_passed": tickers.get(t, {}).get("gate_passed"),
                        "contracts": tickers.get(t, {}).get("contracts"),
                    }
                    for t in ("SPY", "NVDA", "AMZN")
                },
            }
        except Exception as exc:
            report["db"] = {"error": str(exc)}

    # Which is being served
    file_ts = _parse_ts(report["file"].get("written_at") if report["file"] else None)
    db_ts = _parse_ts(report["db"].get("created_at") if report["db"] else None)
    if file_ts and db_ts:
        report["serving"] = "file" if file_ts >= db_ts else "db"
    elif report["file"]:
        report["serving"] = "file"
    elif report["db"]:
        report["serving"] = "db"
    else:
        report["serving"] = "none"

    report["stale_file"] = (
        report["serving"] == "db"
        and report["file"] is not None
        and report["db"] is not None
        and report["db"].get("date") != report["file"].get("date")
    )

    return report


# ── Dashboard page ────────────────────────────────────────────────────────────

def _load_latest_json() -> dict | None:
    """Read the latest run from the git-committed JSON file (survives Render deploys)."""
    try:
        if LATEST_JSON.exists():
            entry = json.loads(LATEST_JSON.read_text())
            if isinstance(entry, dict):
                return entry
    except Exception:
        pass
    return None


def _load_outcome_json() -> dict | None:
    """Read today's EOD outcome if available."""
    try:
        if OUTCOME_JSON.exists():
            data = json.loads(OUTCOME_JSON.read_text())
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return None


@router.get("/options-intel", response_class=HTMLResponse)
async def options_intel_dashboard(request: Request, db: Session = Depends(get_db)):
    """Public dashboard showing the latest morning brief and run history."""
    history: list[dict] = []

    # Parse the git-committed latest.json
    file_latest: dict | None = None
    file_ts: datetime | None = None
    entry = _load_latest_json()
    if entry:
        payload_text = json.dumps({"body": entry.get("body", ""), "structured": entry.get("structured")})
        try:
            file_ts = datetime.fromisoformat(entry.get("written_at", ""))
        except Exception:
            file_ts = None
        file_latest = _parse_brief(payload_text, file_ts)

    # Load SQLite rows (always — used for history and freshness comparison)
    rows = (
        db.query(OptionsIntelNotification)
        .order_by(OptionsIntelNotification.created_at.desc())
        .limit(30)
        .all()
    )
    db_latest: dict | None = None
    db_ts: datetime | None = None
    # Only use morning brief rows as the "latest" source; outcome_brief rows have no snapshot data
    brief_rows = [r for r in rows if r.event_type not in ("outcome_brief",)]
    if brief_rows:
        db_ts = brief_rows[0].created_at
        db_latest = _parse_brief(brief_rows[0].payload_text, db_ts)

    # Pick the NEWER source as latest
    if file_latest and db_latest:
        ft = file_ts.replace(tzinfo=None) if file_ts and file_ts.tzinfo else file_ts
        dt = db_ts.replace(tzinfo=None) if db_ts and db_ts.tzinfo else db_ts
        latest = file_latest if (ft and dt and ft >= dt) else db_latest
    else:
        latest = file_latest or db_latest

    # Build history: start with whichever was newer, merge the other source
    if latest:
        history = [_brief_summary(latest)]
    seen_dates = {h.get("date") for h in history}

    # Supplement history from DB
    db_summaries = [_brief_summary(_parse_brief(r.payload_text, r.created_at)) for r in rows]
    for s in db_summaries:
        if s.get("date") not in seen_dates:
            history.append(s)
            seen_dates.add(s.get("date"))

    # Also include file entry in history if not already present
    if file_latest:
        fs = _brief_summary(file_latest)
        if fs.get("date") not in seen_dates:
            history.insert(0, fs)

    # Load today's EOD outcome if available
    outcome = _load_outcome_json()
    today_str = datetime.now().strftime("%Y-%m-%d")
    if outcome and outcome.get("date") != today_str:
        outcome = None  # stale — don't show yesterday's outcome

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
            "outcome": outcome,
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
        "looking_ahead": None,
        "market_overview": [],
        "market_overview_narrative": None,
        "ticker_horizons": None,
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
        result["looking_ahead"] = structured.get("looking_ahead")
        result["market_overview"] = structured.get("market_overview", [])
        result["market_overview_narrative"] = structured.get("market_overview_narrative")
        result["ticker_horizons"] = structured.get("ticker_horizons")

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

def _parse_ts(ts_str: str | None) -> datetime | None:
    if not ts_str:
        return None
    try:
        dt = datetime.fromisoformat(ts_str)
        return dt.replace(tzinfo=None) if dt.tzinfo else dt
    except Exception:
        return None


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
