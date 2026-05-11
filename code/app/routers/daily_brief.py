import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

EPISODES_FILE = Path(__file__).resolve().parent.parent / "static" / "podcast" / "episodes.json"


def _ctx(request: Request, **kwargs) -> dict:
    return {"request": request, "config": settings, "year": datetime.now().year, **kwargs}


def _load_episodes() -> list[dict]:
    if not EPISODES_FILE.exists():
        return []
    return json.loads(EPISODES_FILE.read_text())["episodes"]


@router.get("/resources/daily-brief", response_class=HTMLResponse)
async def daily_brief_index(request: Request) -> HTMLResponse:
    episodes = _load_episodes()
    return templates.TemplateResponse(
        "resources/daily_brief/index.html",
        _ctx(request, title="Daily Brief — fullstackpm.tech", current_page="/resources", episodes=episodes),
    )


@router.get("/resources/daily-brief/{slug}", response_class=HTMLResponse)
async def daily_brief_episode(request: Request, slug: str) -> HTMLResponse:
    episodes = _load_episodes()
    episode = next((e for e in episodes if e["slug"] == slug), None)
    if not episode:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Not Found", current_page=""),
            status_code=404,
        )
    return templates.TemplateResponse(
        "resources/daily_brief/episode.html",
        _ctx(request, title=f"{episode['title']} — fullstackpm.tech", current_page="/resources", episode=episode),
    )
