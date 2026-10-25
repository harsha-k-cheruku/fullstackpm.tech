"""Forward Catalyst Brief — served at /catalyst-brief."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.config import settings

router = APIRouter()

CATALYST_BRIEF_INDEX = settings.static_dir / "data" / "catalyst_brief" / "index.html"


@router.get("/catalyst-brief", response_class=HTMLResponse)
async def catalyst_brief():
    if not CATALYST_BRIEF_INDEX.exists():
        raise HTTPException(status_code=404, detail="Catalyst brief not found")
    return HTMLResponse(content=CATALYST_BRIEF_INDEX.read_text())
