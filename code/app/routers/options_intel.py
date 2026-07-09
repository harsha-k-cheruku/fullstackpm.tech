"""Webhook receiver for the Daily Options Intelligence System."""
from __future__ import annotations

import json
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.options_intel import OptionsIntelNotification

router = APIRouter(prefix="/api/options-intel", tags=["options-intel"])

MAX_PAYLOAD_BYTES = 256_000


def require_options_intel_token(x_options_intel_token: Optional[str] = Header(default=None)) -> None:
    expected = settings.options_intel_webhook_token
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Options Intel webhook token is not configured",
        )
    if not x_options_intel_token or x_options_intel_token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook token")


@router.post("/notify")
async def capture_notification(
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_options_intel_token),
):
    """Capture one Options Intel notification payload.

    Accepts JSON or text bodies. Requires `X-Options-Intel-Token`.
    """
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


@router.get("/notifications/latest")
async def latest_notification(
    db: Session = Depends(get_db),
    _: None = Depends(require_options_intel_token),
):
    """Return the latest captured notification for verification/debugging."""
    row = db.query(OptionsIntelNotification).order_by(OptionsIntelNotification.created_at.desc()).first()
    if row is None:
        raise HTTPException(status_code=404, detail="No notifications captured yet")
    return row.to_dict()


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
