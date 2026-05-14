from __future__ import annotations

import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))
templates.env.filters["rfc2822"] = lambda v: format_datetime(
    v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v
)

QUESTIONS_FILE = settings.static_dir / "podcast" / "pm-prep" / "episodes.json"
AUDIO_DIR = settings.static_dir / "podcast" / "pm-prep" / "audio"
INTERACTIVE_DIR = settings.static_dir / "podcast" / "pm-prep" / "interactive"


def _load_questions() -> list[dict]:
    if not QUESTIONS_FILE.exists():
        return []
    data = json.loads(QUESTIONS_FILE.read_text())
    return data.get("questions", [])


def _ctx(request: Request, **kw) -> dict:
    return {"request": request, "config": settings, "year": datetime.now().year, **kw}


@router.get("/resources/pm-prep", response_class=HTMLResponse)
async def pm_prep_index(request: Request) -> HTMLResponse:
    questions = _load_questions()
    return templates.TemplateResponse(
        "resources/pm_prep/index.html",
        _ctx(request, title="PM Interview Prep — fullstackpm.tech",
             current_page="/resources", questions=questions),
    )


@router.get("/resources/pm-prep/{question_id}", response_class=HTMLResponse)
async def pm_prep_question(request: Request, question_id: str) -> HTMLResponse:
    questions = _load_questions()
    q = next((x for x in questions if x["id"] == question_id), None)
    if not q:
        return templates.TemplateResponse(
            "404.html", _ctx(request, title="Not Found", current_page=""), status_code=404)
    idx = next(i for i, x in enumerate(questions) if x["id"] == question_id)
    return templates.TemplateResponse(
        "resources/pm_prep/question.html",
        _ctx(request, title=f"PM Prep: {q['question'][:55]}",
             current_page="/resources", question=q,
             prev_question=questions[idx + 1] if idx + 1 < len(questions) else None,
             next_question=questions[idx - 1] if idx > 0 else None),
    )


@router.get("/resources/pm-prep/{question_id}/ep{ep_num:int}", response_class=HTMLResponse)
async def pm_prep_episode(request: Request, question_id: str, ep_num: int) -> HTMLResponse:
    questions = _load_questions()
    q = next((x for x in questions if x["id"] == question_id), None)
    if not q:
        return templates.TemplateResponse(
            "404.html", _ctx(request, title="Not Found", current_page=""), status_code=404)
    eps = q.get("episodes", [])
    ep = next((e for e in eps if e["number"] == ep_num), None)
    if not ep:
        return templates.TemplateResponse(
            "404.html", _ctx(request, title="Not Found", current_page=""), status_code=404)
    # Inject question_id into episode for template use
    ep = {**ep, "question_id": question_id}
    return templates.TemplateResponse(
        "resources/pm_prep/episode.html",
        _ctx(request, title=f"{ep['title']} — fullstackpm.tech",
             current_page="/resources", question=q, episode=ep,
             prev_ep=next((e for e in eps if e["number"] == ep_num - 1), None),
             next_ep=next((e for e in eps if e["number"] == ep_num + 1), None)),
    )


@router.get("/podcast/pm-prep/audio/{filename}")
async def stream_pm_prep_audio(filename: str, request: Request) -> Response:
    import re as _re
    audio_path = AUDIO_DIR / filename
    if not audio_path.exists() or not filename.endswith(".mp3"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    file_size = audio_path.stat().st_size
    range_header = request.headers.get("Range")
    if range_header:
        m = _re.match(r"bytes=(\d+)-(\d*)", range_header)
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else file_size - 1
            end = min(end, file_size - 1)
            chunk = end - start + 1
            with open(audio_path, "rb") as f:
                f.seek(start); data = f.read(chunk)
            return Response(content=data, status_code=206, media_type="audio/mpeg",
                            headers={"Content-Range": f"bytes {start}-{end}/{file_size}",
                                     "Accept-Ranges": "bytes", "Content-Length": str(chunk)})
    return Response(content=audio_path.read_bytes(), media_type="audio/mpeg",
                    headers={"Accept-Ranges": "bytes", "Content-Length": str(file_size)})
