# Feed Layer 3 — Homepage Strip + Audio Brief Pipeline
## Code Puppy Handoff

**Owner:** Harsha
**Validator:** Claude (after completion)
**Depends on:** Layer 2 complete and live (AI scores + editorial dashboard working)
**Goal:** Surface the feed on the homepage, and generate a daily audio brief PM/tech folks can listen to on their commute.

---

## What you are building

**Part A — Homepage Intelligence Strip**
A "Today's Top Stories" section on the homepage showing the 5 highest-scored articles. Appears between the Hero and Newsletter sections. Live, pulls from the same database as `/feed`.

**Part B — Daily Audio Brief**
An automated pipeline that runs once per day:
1. Takes today's top-scored editor's picks (or highest-scored articles if no picks)
2. Generates a ~4-minute podcast script with Claude Haiku
3. Converts script to audio with Edge TTS (Microsoft, free, no API key)
4. Saves the MP3 to `/static/audio/`
5. Updates a manifest file that powers the podcast RSS feed

**Part C — Podcast RSS Feed**
A proper podcast RSS at `/pm-brief.xml` — submittable to Apple Podcasts and Spotify.

---

## Before you start

- Working directory: `/Users/sidc/Projects/claude_code/fullstackpm.tech/`
- All Python files are under `code/app/`
- Layer 2 must be live first — this pipeline depends on `ai_score`, `is_editors_pick`, and the AI insight columns
- `ANTHROPIC_API_KEY` must be set in Render env vars for script generation to work
- Push to `main` at the end — Render auto-deploys
- Commit each step separately

---

## Steps (execute in order)

---

### Step 1 — Add `edge-tts` to requirements.txt

File: `requirements.txt` (top-level)

Add after the `anthropic` line:

```
edge-tts>=6.1.9
```

Commit: `Layer3 Step 1: add edge-tts to requirements`

---

### Step 2 — Create the audio static directory

File: `code/app/static/audio/.gitkeep` (create empty file so git tracks the directory)

Create an empty file at that path. This ensures the audio directory exists for MP3 storage.

Commit: `Layer3 Step 2: add static/audio directory`

---

### Step 3 — Create BriefService

File: `code/app/services/brief_service.py` (new file)

```python
# app/services/brief_service.py
from __future__ import annotations

import asyncio
import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.models.feed_article import FeedArticle

logger = logging.getLogger(__name__)

BRIEF_VOICE = "en-US-AriaNeural"
MAX_STORY_COUNT = 6
MIN_STORY_COUNT = 3

_SCRIPT_SYSTEM = """You are the host of "PM Daily Brief" — a crisp, intelligent 5-minute audio show for senior product managers.

Write a podcast script from the provided top stories. Rules:
- Under 500 words total
- Plain text only — no markdown, no headers, no bullet points
- Conversational but confident — no filler words ("um", "so", "basically", "you know", "kind of")
- Present insights peer-to-peer, not teacher-to-student
- Each story: say the source name, the title or topic, then the key insight naturally woven in, then a brief transition
- Intro: "Good [morning/afternoon]. Here's your PM Intelligence Brief for {date}."
- Outro: "That's your PM brief for today. Full coverage at fullstackpm.tech. Stay sharp."
- Do not add section labels or numbering — just the spoken words"""


def _build_script_prompt(articles: list[FeedArticle], brief_date: str) -> str:
    stories = []
    for a in articles:
        insight = a.ai_summary or a.first_principle or a.key_insight or a.ai_insight or a.excerpt or ""
        stories.append({
            "source": a.source_name,
            "category": a.source_category,
            "title": a.title,
            "score": a.ai_score,
            "insight": insight[:300],
        })
    return (
        f"Date: {brief_date}\n\n"
        f"Top stories ({len(stories)}):\n"
        + json.dumps(stories, indent=2)
        + "\n\nWrite the podcast script now."
    )


def _get_audio_dir() -> Path:
    audio_dir = settings.static_dir / "audio"
    audio_dir.mkdir(exist_ok=True)
    return audio_dir


def _get_manifest_path() -> Path:
    return _get_audio_dir() / "pm-brief-manifest.json"


def _load_manifest() -> dict:
    path = _get_manifest_path()
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return {"episodes": []}


def _save_manifest(manifest: dict) -> None:
    _get_manifest_path().write_text(json.dumps(manifest, indent=2, default=str))


def _today_brief_exists() -> bool:
    today = date.today().isoformat()
    manifest = _load_manifest()
    return any(ep.get("date") == today for ep in manifest.get("episodes", []))


class BriefService:
    async def generate_if_needed(self, db: Session) -> bool:
        """Generate today's brief if it doesn't exist yet. Returns True if generated."""
        if _today_brief_exists():
            logger.info("Today's PM brief already exists — skipping")
            return False
        return await self.generate(db)

    async def generate(self, db: Session) -> bool:
        """Generate a fresh brief for today. Returns True on success."""
        articles = self._get_brief_articles(db)
        if len(articles) < MIN_STORY_COUNT:
            logger.warning("Not enough scored articles for brief (got %d, need %d)", len(articles), MIN_STORY_COUNT)
            return False

        today = date.today()
        brief_date = today.strftime("%B %d, %Y")
        date_slug = today.isoformat()
        audio_filename = f"pm-brief-{date_slug}.mp3"
        audio_path = _get_audio_dir() / audio_filename

        script = self._generate_script(articles, brief_date)
        if not script:
            logger.error("Script generation failed — skipping audio")
            return False

        success = await self._generate_audio(script, audio_path)
        if not success:
            return False

        self._update_manifest(
            date_slug=date_slug,
            title=f"PM Daily Brief — {brief_date}",
            audio_filename=audio_filename,
            article_count=len(articles),
            script=script,
        )
        logger.info("PM brief generated: %s (%d stories)", audio_filename, len(articles))
        return True

    def _get_brief_articles(self, db: Session) -> list[FeedArticle]:
        picks = (
            db.query(FeedArticle)
            .filter(
                FeedArticle.is_editors_pick == True,
                FeedArticle.is_dismissed == False,
                FeedArticle.ai_score.isnot(None),
            )
            .order_by(FeedArticle.ai_score.desc())
            .limit(MAX_STORY_COUNT)
            .all()
        )
        if len(picks) >= MIN_STORY_COUNT:
            return picks

        # Fallback: top-scored articles from today/recent
        return (
            db.query(FeedArticle)
            .filter(
                FeedArticle.is_dismissed == False,
                FeedArticle.ai_score >= 7,
            )
            .order_by(FeedArticle.ai_score.desc(), FeedArticle.fetched_at.desc())
            .limit(MAX_STORY_COUNT)
            .all()
        )

    def _generate_script(self, articles: list[FeedArticle], brief_date: str) -> Optional[str]:
        if not settings.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY not set — using excerpt-only script")
            return self._fallback_script(articles, brief_date)
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=settings.anthropic_api_key)
            response = client.messages.create(
                model=settings.anthropic_model,
                max_tokens=700,
                system=_SCRIPT_SYSTEM,
                messages=[{"role": "user", "content": _build_script_prompt(articles, brief_date)}],
            )
            return response.content[0].text.strip()
        except Exception as exc:
            logger.error("Script generation failed: %s", exc)
            return self._fallback_script(articles, brief_date)

    def _fallback_script(self, articles: list[FeedArticle], brief_date: str) -> str:
        lines = [f"Good morning. Here's your PM Intelligence Brief for {brief_date}."]
        for a in articles:
            insight = a.ai_summary or a.first_principle or a.key_insight or a.ai_insight or a.excerpt or ""
            lines.append(f"From {a.source_name}: {a.title}. {insight}")
        lines.append("That's your PM brief for today. Full coverage at fullstackpm.tech. Stay sharp.")
        return " ".join(lines)

    async def _generate_audio(self, script: str, output_path: Path) -> bool:
        try:
            import edge_tts
            communicate = edge_tts.Communicate(script, BRIEF_VOICE)
            await communicate.save(str(output_path))
            return True
        except Exception as exc:
            logger.error("Edge TTS audio generation failed: %s", exc)
            return False

    def _update_manifest(
        self,
        date_slug: str,
        title: str,
        audio_filename: str,
        article_count: int,
        script: str,
    ) -> None:
        manifest = _load_manifest()
        audio_url = f"{settings.site_url}/static/audio/{audio_filename}"
        episode = {
            "date": date_slug,
            "title": title,
            "audio_url": audio_url,
            "audio_filename": audio_filename,
            "article_count": article_count,
            "script": script,
            "generated_at": datetime.utcnow().isoformat(),
        }
        episodes = [ep for ep in manifest.get("episodes", []) if ep.get("date") != date_slug]
        episodes.insert(0, episode)
        manifest["episodes"] = episodes[:30]
        _save_manifest(manifest)

    def get_latest(self) -> Optional[dict]:
        """Return the most recent episode from the manifest."""
        manifest = _load_manifest()
        episodes = manifest.get("episodes", [])
        return episodes[0] if episodes else None

    def get_all(self) -> list[dict]:
        """Return all episodes from the manifest."""
        return _load_manifest().get("episodes", [])


brief_service = BriefService()
```

Commit: `Layer3 Step 3: add BriefService (script generation + Edge TTS audio)`

---

### Step 4 — Wire BriefService into main.py startup and background loop

File: `code/app/main.py`

**4a. Add import** with the other service imports:

```python
from app.services.brief_service import brief_service
```

**4b. Update startup block** — the startup is in an async lifespan so `await` works:

```python
    # Feed: initial fetch + AI processing + daily brief
    db = SessionLocal()
    try:
        feed_service.fetch_all(db)
        ai_processing_service.process_unprocessed(db)
        await brief_service.generate_if_needed(db)
    finally:
        db.close()
```

**4c. Update `_refresh_loop`** — same pattern:

```python
    async def _refresh_loop():
        while True:
            await asyncio.sleep(6 * 3600)
            db = SessionLocal()
            try:
                feed_service.fetch_all(db)
                ai_processing_service.process_unprocessed(db)
                await brief_service.generate_if_needed(db)
            finally:
                db.close()
```

Commit: `Layer3 Step 4: wire brief generation into startup and background refresh`

---

### Step 5 — Add manual brief generation endpoint to feed router

File: `code/app/routers/feed.py`

**5a. Add import** at the top:

```python
from app.services.brief_service import brief_service
```

**5b. Add endpoint** after the existing `/api/feed/refresh` endpoint:

```python
@router.post("/api/feed/brief/generate", response_class=JSONResponse)
async def generate_brief(token: str = "", db: Session = Depends(get_db)):
    """Manually trigger a fresh audio brief generation."""
    _check_editorial_token(token)
    success = await brief_service.generate(db)
    latest = brief_service.get_latest()
    return {
        "status": "ok" if success else "error",
        "generated": success,
        "latest": latest,
    }
```

Commit: `Layer3 Step 5: add /api/feed/brief/generate manual trigger endpoint`

---

### Step 6 — Add podcast RSS route to feed router

File: `code/app/routers/feed.py`

**6a. Add Response to FastAPI imports** — update the import line at the top:

```python
from fastapi import APIRouter, Depends, HTTPException, Request, Response
```

**6b. Add endpoint** after the brief generate endpoint:

```python
@router.get("/pm-brief.xml")
async def podcast_rss():
    """Podcast RSS feed for PM Daily Brief."""
    episodes = brief_service.get_all()
    items = ""
    for ep in episodes:
        pub_date = ""
        try:
            dt = datetime.fromisoformat(ep.get("generated_at", ""))
            pub_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except Exception:
            pass
        audio_url = ep.get("audio_url", "")
        items += f"""
    <item>
      <title>{ep.get("title", "")}</title>
      <description>{ep.get("article_count", 0)} top PM stories, scored and distilled.</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}" type="audio/mpeg"/>
      <guid>{audio_url}</guid>
    </item>"""

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>PM Daily Brief</title>
    <link>https://fullstackpm.tech</link>
    <description>Daily intelligence brief for product managers — top stories from PM, engineering, strategy, and AI, distilled to essentials by fullstackpm.tech.</description>
    <language>en-us</language>
    <itunes:author>Harsha Cheruku</itunes:author>
    <itunes:category text="Technology"/>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="https://fullstackpm.tech/static/img/FSPM.png"/>
    <image>
      <url>https://fullstackpm.tech/static/img/FSPM.png</url>
      <title>PM Daily Brief</title>
      <link>https://fullstackpm.tech</link>
    </image>{items}
  </channel>
</rss>"""
    return Response(content=rss, media_type="application/rss+xml")
```

Commit: `Layer3 Step 6: add /pm-brief.xml podcast RSS feed`

---

### Step 7 — Pass top articles and latest brief to homepage

File: `code/app/routers/pages.py`

**7a. Add imports** at the top:

```python
from app.database import get_db, SessionLocal
from app.services.feed_service import feed_service
from app.services.brief_service import brief_service
```

**7b. Replace the `home` route** with:

```python
@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Consolidated home page: Full Stack PM definition + components."""
    content_service = request.app.state.content_service
    reading_service = request.app.state.reading_service
    recent_posts, _ = content_service.get_posts(page=1, per_page=3)
    reading = reading_service.get()

    db = SessionLocal()
    try:
        top_articles = feed_service.get_articles(db, limit=5)
    finally:
        db.close()

    latest_brief = brief_service.get_latest()

    return templates.TemplateResponse(
        "index.html",
        _ctx(
            request,
            title="@fullstackpm - Harsha Cheruku",
            current_page="/",
            recent_posts=recent_posts,
            reading=reading,
            top_articles=top_articles,
            latest_brief=latest_brief,
        ),
    )
```

Commit: `Layer3 Step 7: pass top_articles and latest_brief to homepage`

---

### Step 8 — Add Intelligence Strip and Audio Player to homepage

File: `code/app/templates/index.html`

Insert two new sections between the `<!-- HERO -->` closing `</section>` tag (line 29) and the `<!-- NEWSLETTER SIGNUP -->` section (line 32).

**Insert after line 29 (after the hero `</section>`):**

```html
<!-- PM INTELLIGENCE STRIP -->
{% if top_articles %}
<section style="padding: 2.5rem 0; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-5xl mx-auto px-6">
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:8px;">
      <div style="display:flex;align-items:baseline;gap:12px;">
        <h2 style="font-size:1rem;font-weight:800;letter-spacing:-0.01em;color:var(--color-text-primary);">Today's Intelligence</h2>
        <span style="font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background-color:var(--color-accent);color:#fff;">Live</span>
      </div>
      <a href="/feed" style="font-size:0.8rem;font-weight:600;color:var(--color-accent);text-decoration:none;">Full feed &rarr;</a>
    </div>

    <div style="display:flex;flex-direction:column;gap:10px;">
      {% for article in top_articles %}
      <a href="{{ article.url }}" target="_blank" rel="noopener noreferrer"
         style="display:flex;align-items:flex-start;gap:14px;padding:14px 18px;border:1px solid var(--color-border);border-radius:10px;text-decoration:none;"
         class="card-hover">

        <!-- Score -->
        {% if article.ai_score %}
        <div style="min-width:36px;text-align:center;flex-shrink:0;padding-top:2px;">
          <div style="font-size:0.9rem;font-weight:800;color:{{ '#16a34a' if article.ai_score >= 8 else ('#d97706' if article.ai_score >= 5 else '#9ca3af') }};">{{ article.ai_score }}</div>
          <div style="font-size:9px;color:var(--color-text-tertiary);">/10</div>
        </div>
        {% endif %}

        <!-- Content -->
        <div style="flex:1;min-width:0;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;flex-wrap:wrap;">
            {% if article.source_category == 'pm' %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:1px 7px;border-radius:999px;background-color:var(--color-blue-100);color:var(--color-blue-900);">PM</span>
            {% elif article.source_category == 'engineering' %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:1px 7px;border-radius:999px;background-color:var(--color-success-100);color:var(--color-success-900);">ENG</span>
            {% elif article.source_category == 'ai' %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:1px 7px;border-radius:999px;background-color:#ede9fe;color:#5b21b6;">AI</span>
            {% else %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:1px 7px;border-radius:999px;background-color:var(--color-warning-100);color:var(--color-warning-900);">STRATEGY</span>
            {% endif %}
            {% if article.is_editors_pick %}
            <span style="font-size:9px;font-weight:700;color:#d97706;">★ Pick</span>
            {% endif %}
            <span style="font-size:11px;color:var(--color-text-tertiary);">{{ article.source_name }}</span>
          </div>
          <p style="font-size:0.9rem;font-weight:600;color:var(--color-text-primary);line-height:1.4;margin:0;">{{ article.title }}</p>
          {% set insight = article.ai_summary or article.first_principle or article.key_insight or article.ai_insight %}
          {% if insight %}
          <p style="font-size:0.8rem;color:var(--color-text-secondary);margin-top:4px;line-height:1.45;">{{ insight[:150] }}{% if insight|length > 150 %}…{% endif %}</p>
          {% endif %}
        </div>
      </a>
      {% endfor %}
    </div>
  </div>
</section>
{% endif %}

<!-- AUDIO BRIEF -->
{% if latest_brief %}
<section style="padding: 2rem 0; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-5xl mx-auto px-6">
    <div style="border:1px solid var(--color-border);border-radius:12px;padding:20px 24px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
      <div style="flex:1;min-width:200px;">
        <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--color-accent);margin-bottom:4px;">PM Daily Brief</p>
        <p style="font-size:0.95rem;font-weight:700;color:var(--color-text-primary);margin-bottom:4px;">{{ latest_brief.title }}</p>
        <p style="font-size:0.8rem;color:var(--color-text-tertiary);">{{ latest_brief.article_count }} stories &middot; ~5 min &middot; <a href="/pm-brief.xml" style="color:var(--color-accent);">Subscribe via RSS</a></p>
      </div>
      <div style="flex-shrink:0;">
        <audio controls style="height:36px;width:260px;max-width:100%;">
          <source src="{{ latest_brief.audio_url }}" type="audio/mpeg">
          Your browser does not support audio.
        </audio>
      </div>
    </div>
  </div>
</section>
{% endif %}
```

Commit: `Layer3 Step 8: add intelligence strip and audio brief player to homepage`

---

### Step 9 — Push and verify

```bash
git push origin main
```

After Render deploys (~2 min):

1. Visit `https://fullstackpm.tech` — homepage should show "Today's Intelligence" strip with top 5 articles
2. Audio player appears once a brief has been generated (trigger manually via editorial dashboard or wait for next startup)
3. To trigger brief generation manually:
   ```
   curl -X POST "https://fullstackpm.tech/api/feed/brief/generate?token=fspm-editorial-2026"
   ```
4. After generation, audio player appears on homepage with today's brief
5. Visit `https://fullstackpm.tech/pm-brief.xml` — podcast RSS should be valid XML with episode entries
6. Check Render logs for any Edge TTS errors

---

## Results (fill in after completing)

| Step | Status | Notes |
|------|--------|-------|
| 1 — Add edge-tts to requirements | done | Added `edge-tts>=6.1.9`; committed `733ac9d`. |
| 2 — Create static/audio dir | done | Added `code/app/static/audio/.gitkeep`; committed `a0e246a`. |
| 3 — BriefService | done | Added script generation, fallback script, Edge TTS audio generation, and manifest management; committed `d663c45`. |
| 4 — Wire into startup + refresh loop | done | Startup and 6-hour refresh now call `brief_service.generate_if_needed`; committed `bf24ccb`. |
| 5 — Manual generate endpoint | done | Added token-gated `POST /api/feed/brief/generate`; committed `7629a62`. |
| 6 — Podcast RSS route | done | Added `/pm-brief.xml` RSS feed with XML escaping; committed `f8d4e71`. |
| 7 — Pass data to homepage | done | Homepage now receives `top_articles` and `latest_brief`; committed `e529735`. |
| 8 — Homepage template sections | done | Added Today's Intelligence strip and conditional audio player; committed `f3b3d7c`. |
| 9 — Push + verify | partial | Pushed to `main`. Live homepage returns 200 and shows Today's Intelligence. `/pm-brief.xml` returns 200 RSS. Manual brief endpoint returns 200 but `generated:false` / `latest:null` because prod does not currently have enough scored articles. This likely depends on Render `ANTHROPIC_API_KEY` being set so Layer 2 can populate `ai_score`. |

---

## Blockers reference

- **`edge_tts` ImportError**: not in requirements.txt — check Step 1
- **Audio player shows but no sound**: audio file path wrong — check `/static/audio/` dir exists and MP3 was written
- **Brief not generating**: check Render logs for "ANTHROPIC_API_KEY not set" warning; fallback script still runs Edge TTS, so audio should still be generated even without Claude
- **Homepage strip empty**: `top_articles` not passed — check Step 7 (pages.py update)
- **Podcast RSS returns 404**: route not registered — confirm `feed.router` is included in main.py (it already is)
- **Edge TTS fails on Render**: Edge TTS makes outbound calls to Microsoft servers; Render allows these by default. If blocked, check Render's network settings

---

## What comes next (Layer 4 — future scope, do not build now)

- **ElevenLabs voice clone**: swap Edge TTS for Harsha's cloned voice — same script, different TTS call
- **Weekly editorial digest**: email newsletter auto-drafted from the week's top picks, sent via Kit API
- **Personalized feed**: per-user topic preferences stored in browser localStorage, filtered feed view
- **Homepage "Editor's Note"**: one-paragraph editorial comment written by Harsha, displayed above the strip
