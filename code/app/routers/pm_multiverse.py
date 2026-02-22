import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.config import settings
from app.database import get_db
from app.models.pm_multiverse import PmmVote

router = APIRouter()

PROBLEMS_DIR = settings.static_dir / "data" / "pmm" / "problems"
STATIC_PMM = settings.static_dir / "pmm"

VALID_PERSONAS = {"cagan", "torres", "doshi", "lenny", "exec"}


# ── Pages ────────────────────────────────────────────────────────

@router.get("/tools/pm-multiverse")
async def pmm_index():
    return FileResponse(str(STATIC_PMM / "index.html"))


@router.get("/tools/pm-multiverse/problem")
async def pmm_problem():
    return FileResponse(str(STATIC_PMM / "problem.html"))


# ── API ──────────────────────────────────────────────────────────

@router.get("/api/pmm/problems")
async def list_problems():
    problems = []
    for f in sorted(PROBLEMS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            problems.append({
                "id": data["id"],
                "title": data["title"],
                "tags": data.get("tags", []),
                "prompt": data.get("prompt", ""),
                "file": f.name,
            })
        except Exception:
            continue
    return problems


class VoteCreate(BaseModel):
    problem_id: str
    persona: str


def _vote_counts(db: Session, problem_id: str) -> dict:
    rows = (
        db.query(PmmVote.persona, func.count(PmmVote.id))
        .filter(PmmVote.problem_id == problem_id)
        .group_by(PmmVote.persona)
        .all()
    )
    return {persona: count for persona, count in rows}


@router.get("/api/pmm/votes/{problem_id}")
async def get_votes(problem_id: str, db: Session = Depends(get_db)):
    return _vote_counts(db, problem_id)


@router.post("/api/pmm/votes")
async def cast_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    if vote.persona not in VALID_PERSONAS:
        raise HTTPException(status_code=400, detail="Invalid persona")
    if not vote.problem_id:
        raise HTTPException(status_code=400, detail="problem_id required")

    db.add(PmmVote(problem_id=vote.problem_id, persona=vote.persona))
    db.commit()
    return _vote_counts(db, vote.problem_id)
