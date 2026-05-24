import json
import markdown as md_lib
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

EPISODES_FILE = Path(__file__).resolve().parent.parent / "static" / "podcast" / "the-backstory" / "episodes.json"


def _ctx(request: Request, **kwargs) -> dict:
    return {"request": request, "config": settings, "year": datetime.now().year, **kwargs}


def _load_episodes() -> list[dict]:
    if not EPISODES_FILE.exists():
        return []
    return json.loads(EPISODES_FILE.read_text())["episodes"]


@router.get("/resources/the-backstory", response_class=HTMLResponse)
async def backstory_index(request: Request) -> HTMLResponse:
    episodes = _load_episodes()
    return templates.TemplateResponse(
        "resources/backstory/index.html",
        _ctx(request, title="The Backstory — fullstackpm.tech", current_page="/resources", episodes=episodes),
    )


@router.get("/resources/the-backstory/{slug}", response_class=HTMLResponse)
async def backstory_episode(request: Request, slug: str) -> HTMLResponse:
    episodes = _load_episodes()
    episode = next((e for e in episodes if e["slug"] == slug), None)
    if not episode:
        return templates.TemplateResponse(
            "404.html",
            _ctx(request, title="Not Found", current_page=""),
            status_code=404,
        )
    if "shownotes_html" not in episode and "shownotes" in episode:
        episode = dict(episode)
        episode["shownotes_html"] = md_lib.markdown(episode["shownotes"], extensions=["nl2br"])
    return templates.TemplateResponse(
        "resources/backstory/episode.html",
        _ctx(request, title=f"{episode['title']} — fullstackpm.tech", current_page="/resources", episode=episode),
    )
