"""Market Pulse — intraday market update served at /market-pulse."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.config import settings

router = APIRouter()

MARKET_PULSE_INDEX = settings.static_dir / "data" / "market_pulse" / "index.html"


@router.get("/market-pulse", response_class=HTMLResponse)
async def market_pulse():
    if not MARKET_PULSE_INDEX.exists():
        raise HTTPException(status_code=404, detail="Market pulse not found")
    return HTMLResponse(content=MARKET_PULSE_INDEX.read_text())
