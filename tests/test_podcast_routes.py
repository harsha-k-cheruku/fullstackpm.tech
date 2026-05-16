from __future__ import annotations

import json
import os
from datetime import datetime
from io import BytesIO

from fastapi.testclient import TestClient

from app.database import SessionLocal, init_db
from app.main import app
from app.models.episode import Episode

client = TestClient(app)


def _seed_episode() -> None:
    db = SessionLocal()
    if not db.query(Episode).filter(Episode.id == "2026-05-10").first():
        db.add(Episode(
            id="2026-05-10",
            slug="daily-brief-2026-05-10",
            episode_number=1,
            title="Daily Brief — May 10, 2026",
            date=datetime(2026, 5, 10),
            published_at=datetime(2026, 5, 10, 5, 28),
            duration_seconds=1500,
            duration_human="25:00",
            audio_url="https://fullstackpm.tech/static/podcast/audio/2026-05-10.mp3",
            shownotes_html="<p>Notes</p>",
            curriculum_lesson="What is Delta",
            spy_close=512.34,
            spy_pct_change=0.42,
            iv_rank=32.0,
            tags=json.dumps(["SPY", "options"]),
            status="complete",
        ))
        db.commit()
    db.close()


init_db()
_seed_episode()


def test_podcast_unknown_slug_returns_404() -> None:
    response = client.get("/podcast/does-not-exist")
    assert response.status_code == 404


def test_feed_xml_returns_rss() -> None:
    response = client.get("/podcast/feed.xml")
    assert response.status_code == 200
    assert "application/rss+xml" in response.headers["content-type"]
    assert "<rss" in response.text


def test_api_requires_auth() -> None:
    response = client.post(
        "/api/narada/episode",
        data={"episode_json": json.dumps({}), "shownotes_md": "# hi"},
        files={"audio": ("episode.mp3", BytesIO(b"audio"), "audio/mpeg")},
    )
    assert response.status_code == 401
