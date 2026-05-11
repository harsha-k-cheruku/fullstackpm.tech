from __future__ import annotations

import json
import os
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from typing import List, Optional

import markdown
from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.episode import Episode

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))
templates.env.filters["rfc2822"] = lambda value: format_datetime(value)
AUDIO_DIR = settings.static_dir / "podcast" / "audio"
EPISODES_FILE = settings.static_dir / "podcast" / "episodes.json"


def _load_episodes_json() -> list[dict]:
    """Load episodes from JSON file — source of truth until remote publish populates the DB."""
    if not EPISODES_FILE.exists():
        return []
    return json.loads(EPISODES_FILE.read_text()).get("episodes", [])


def _ctx(request: Request, **kwargs) -> dict:
    return {"request": request, "config": settings, "year": datetime.now().year, **kwargs}


def _group_by_month(episodes: List[Episode]) -> list[dict]:
    grouped: list[dict] = []
    current_month = ""
    for episode in episodes:
        month = episode.date.strftime("%B %Y")
        if month != current_month:
            current_month = month
            grouped.append({"month": month, "episodes": []})
        grouped[-1]["episodes"].append(episode)
    return grouped


def _parse_tags(raw_tags: Optional[str]) -> List[str]:
    if not raw_tags:
        return []
    try:
        value = json.loads(raw_tags)
        return [str(tag) for tag in value]
    except Exception:
        return [tag.strip() for tag in raw_tags.split(",") if tag.strip()]


@router.get("/podcast", response_class=HTMLResponse)
async def podcast_list(request: Request) -> HTMLResponse:
    episodes = _load_episodes_json()
    tags = sorted({tag for ep in episodes for tag in ep.get("tags", [])}, key=str.lower)
    return templates.TemplateResponse(
        "podcast/list.html",
        _ctx(request, title="Daily Brief — fullstackpm.tech", current_page="/podcast", episodes=episodes, tags=tags),
    )


@router.get("/podcast/feed.xml")
async def podcast_feed(request: Request) -> Response:
    episodes = _load_episodes_json()
    # Parse date strings into datetime objects for the RSS template
    for ep in episodes:
        if isinstance(ep.get("date"), str):
            try:
                ep["date_dt"] = datetime.fromisoformat(ep["date"])
            except Exception:
                ep["date_dt"] = datetime.now()
        else:
            ep["date_dt"] = datetime.now()
    xml = templates.get_template("podcast/feed.xml").render(
        _ctx(request, episodes=episodes, title="Daily Brief — fullstackpm.tech", current_page="/podcast")
    )
    return Response(content=xml, media_type="application/rss+xml")


@router.get("/podcast/{slug}", response_class=HTMLResponse)
async def podcast_detail(request: Request, slug: str) -> HTMLResponse:
    episodes = _load_episodes_json()
    episode = next((e for e in episodes if e.get("slug") == slug), None)
    if not episode:
        return templates.TemplateResponse("404.html", _ctx(request, title="Page Not Found", current_page=""), status_code=404)
    index = next((i for i, e in enumerate(episodes) if e.get("slug") == slug), 0)
    return templates.TemplateResponse(
        "podcast/detail.html",
        _ctx(
            request,
            title=f"{episode['title']} — Daily Brief",
            current_page="/podcast",
            episode=episode,
            previous_episode=episodes[index + 1] if index + 1 < len(episodes) else None,
            next_episode=episodes[index - 1] if index > 0 else None,
            tags=episode.get("tags", []),
        ),
    )


@router.post("/api/narada/episode")
async def receive_episode(
    request: Request,
    episode_json: str = Form(...),
    shownotes_md: str = Form(...),
    audio: UploadFile = File(...),
    x_narada_key: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> dict:
    expected = os.getenv("NARADA_API_KEY", "")
    if not expected or x_narada_key != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    payload = json.loads(episode_json)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_filename = f"{payload['id']}.mp3"
    audio_path = AUDIO_DIR / audio_filename
    audio_bytes = await audio.read()
    audio_path.write_bytes(audio_bytes)

    shownotes_html = markdown.markdown(shownotes_md, extensions=["extra", "smarty"])
    episode = db.query(Episode).filter(Episode.id == payload["id"]).first()
    if episode is None:
        episode = Episode(id=payload["id"], slug=payload["slug"], episode_number=int(payload["episode_number"]), title=payload["title"], date=datetime.fromisoformat(payload["date"]), published_at=datetime.fromisoformat(payload["published_at"]), audio_url=f"{settings.site_url}/static/podcast/audio/{audio_filename}")
        db.add(episode)

    episode.slug = payload["slug"]
    episode.episode_number = int(payload["episode_number"])
    episode.title = payload["title"]
    episode.date = datetime.fromisoformat(payload["date"])
    episode.published_at = datetime.fromisoformat(payload["published_at"])
    episode.duration_seconds = payload.get("duration_seconds")
    episode.duration_human = payload.get("duration_human")
    episode.audio_url = f"{settings.site_url}/static/podcast/audio/{audio_filename}"
    episode.shownotes_html = shownotes_html
    episode.curriculum_lesson = payload.get("curriculum", {}).get("lesson", "")
    episode.spy_close = payload.get("spy_stats", {}).get("close")
    episode.spy_pct_change = payload.get("spy_stats", {}).get("pct_change")
    episode.iv_rank = payload.get("spy_stats", {}).get("iv_rank")
    episode.tags = json.dumps(payload.get("tags", []))
    episode.status = payload.get("status", "complete")
    db.commit()
    return {"status": "ok", "slug": episode.slug, "url": f"{settings.site_url}/podcast/{episode.slug}"}
