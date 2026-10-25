"""Project Artha — SPY options paper trading journal at /artha."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.config import settings

router = APIRouter()

ARTHA_INDEX = settings.static_dir / "data" / "artha" / "index.html"


@router.get("/artha", response_class=HTMLResponse)
async def artha():
    if not ARTHA_INDEX.exists():
        raise HTTPException(status_code=404, detail="Artha journal not found")
    return HTMLResponse(content=ARTHA_INDEX.read_text())
