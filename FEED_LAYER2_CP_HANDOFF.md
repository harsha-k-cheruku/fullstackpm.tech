# Feed Layer 2 + Editorial Dashboard — Code Puppy Handoff

**Owner:** Harsha
**Validator:** Claude (after completion)
**Goal:** Add AI scoring + editorial review dashboard to the PM Intelligence Feed.

---

## What you are building

Two things:

1. **Layer 2 AI processing** — every ingested article gets scored 1–10 for PM relevance and annotated with a category-specific insight (PM Take / First Principle / Key Insight / AI for PMs). Runs automatically after each feed refresh.

2. **Editorial dashboard** at `/feed/editorial` — a private page (token-gated) where the owner reviews articles sorted by AI score, marks Editor's Picks, or dismisses low-quality ones.

---

## Before you start

- Working directory: `/Users/sidc/Projects/claude_code/fullstackpm.tech/`
- All Python files are under `code/app/`
- Push to `main` at the end — Render auto-deploys
- Commit each step separately with a clear message
- `anthropic` SDK is NOT yet in `requirements.txt` — Step 1 adds it
- `ANTHROPIC_API_KEY` and `EDITORIAL_TOKEN` must be set in Render env vars before deploy — note this in your results

---

## Steps (execute in order)

---

### Step 1 — Add `anthropic` to requirements.txt

File: `requirements.txt` (top-level, next to `code/`)

Add this line anywhere in the file:

```
anthropic>=0.40.0
```

Commit: `Layer2 Step 1: add anthropic SDK to requirements`

---

### Step 2 — Add config keys

File: `code/app/config.py`

Inside the `Settings` class, after `openai_max_tokens`, add:

```python
    # Anthropic API (for feed AI processing)
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-4-5-20251001"

    # Editorial dashboard token (set via env var EDITORIAL_TOKEN)
    editorial_token: str = "fspm-editorial-2026"
```

Commit: `Layer2 Step 2: add anthropic_api_key and editorial_token to config`

---

### Step 3 — Extend FeedArticle model + add migration helper

**3a. Update the model**

File: `code/app/models/feed_article.py`

Replace the entire file with:

```python
# app/models/feed_article.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class FeedArticle(Base):
    __tablename__ = "feed_articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    excerpt = Column(Text, nullable=True)
    source_name = Column(String(200), nullable=False)
    source_category = Column(String(50), nullable=False)
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    is_editors_pick = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)

    # Layer 2: AI enrichment
    ai_summary = Column(Text, nullable=True)        # engineering: PM-lens explanation
    first_principle = Column(Text, nullable=True)   # strategy: mental model extraction
    key_insight = Column(Text, nullable=True)       # pm: actionable takeaway
    ai_insight = Column(Text, nullable=True)        # ai: so what for PMs
    ai_score = Column(Integer, nullable=True)       # 1–10 PM relevance score
    ai_score_reason = Column(Text, nullable=True)   # one sentence explaining score
    ai_processed_at = Column(DateTime, nullable=True)
```

**3b. Add migration helper to database.py**

File: `code/app/database.py`

After the existing `init_db()` function, add:

```python
def ensure_feed_layer2_columns() -> None:
    """Idempotent migration: add Layer 2 columns to feed_articles if missing."""
    from sqlalchemy import inspect, text

    existing = {col["name"] for col in inspect(engine).get_columns("feed_articles")}
    new_columns = {
        "is_dismissed": "ALTER TABLE feed_articles ADD COLUMN is_dismissed BOOLEAN DEFAULT 0",
        "ai_summary": "ALTER TABLE feed_articles ADD COLUMN ai_summary TEXT",
        "first_principle": "ALTER TABLE feed_articles ADD COLUMN first_principle TEXT",
        "key_insight": "ALTER TABLE feed_articles ADD COLUMN key_insight TEXT",
        "ai_insight": "ALTER TABLE feed_articles ADD COLUMN ai_insight TEXT",
        "ai_score": "ALTER TABLE feed_articles ADD COLUMN ai_score INTEGER",
        "ai_score_reason": "ALTER TABLE feed_articles ADD COLUMN ai_score_reason TEXT",
        "ai_processed_at": "ALTER TABLE feed_articles ADD COLUMN ai_processed_at DATETIME",
    }
    with engine.begin() as conn:
        for column, statement in new_columns.items():
            if column not in existing:
                conn.execute(text(statement))
```

Commit: `Layer2 Step 3: extend FeedArticle model + add migration helper`

---

### Step 4 — Wire migration into startup

File: `code/app/main.py`

**4a. Add import** — after the existing `from app.database import SessionLocal, init_db` line:

```python
from app.database import SessionLocal, init_db, ensure_feed_layer2_columns
```

**4b. Call migration** — in the `lifespan()` function, after `init_db()`:

```python
    init_db()
    ensure_feed_layer2_columns()
```

Commit: `Layer2 Step 4: call migration helper on startup`

---

### Step 5 — Create AIProcessingService

File: `code/app/services/ai_processing_service.py` (new file)

```python
# app/services/ai_processing_service.py
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.models.feed_article import FeedArticle

logger = logging.getLogger(__name__)

MAX_ARTICLES_PER_RUN = 20
MAX_INSIGHT_CHARS = 400

_SYSTEM_PROMPT = """You are a senior product manager analyst. Given an article title and excerpt, return a JSON object with exactly these keys:
- "score": integer 1-10 (PM relevance: 8-10 = directly actionable or strategically important for a senior B2B SaaS PM; 5-7 = interesting but not urgent; 1-4 = too niche, too technical, or too generic)
- "score_reason": one sentence explaining the score
- "insight": a short insight tailored to the category:
  - engineering: explain what changed and what PMs should understand about the trade-off (under 80 words)
  - strategy: name the first-principles mental model this illustrates and why it matters (under 60 words)
  - pm: the single most actionable takeaway for a practising PM (one sentence)
  - ai: what this means for PMs in practical terms — opportunity or risk (under 60 words)

Return only valid JSON. No markdown fences, no extra text."""


def _build_prompt(article: FeedArticle) -> str:
    return (
        f"Category: {article.source_category}\n"
        f"Source: {article.source_name}\n"
        f"Title: {article.title}\n"
        f"Excerpt: {article.excerpt or '(no excerpt)'}\n\n"
        "Return the JSON object."
    )


class AIProcessingService:
    def process_unprocessed(self, db: Session, limit: int = MAX_ARTICLES_PER_RUN) -> int:
        """Process unprocessed articles. Returns count successfully enriched."""
        if not settings.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY not set — skipping AI processing")
            return 0

        articles = (
            db.query(FeedArticle)
            .filter(FeedArticle.ai_processed_at.is_(None))
            .order_by(FeedArticle.fetched_at.desc())
            .limit(limit)
            .all()
        )

        count = 0
        for article in articles:
            try:
                result = self._process_article(article)
                if result:
                    article.ai_processed_at = datetime.utcnow()
                    db.commit()
                    count += 1
            except Exception as exc:
                logger.warning("AI processing failed for article %s: %s", article.id, exc)
                db.rollback()

        return count

    def _process_article(self, article: FeedArticle) -> bool:
        raw = self._call_claude(_build_prompt(article))
        if not raw:
            return False

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON from Claude for article %s: %s", article.id, raw[:200])
            return False

        article.ai_score = int(data.get("score", 0)) or None
        article.ai_score_reason = (data.get("score_reason") or "")[:500] or None

        insight = (data.get("insight") or "")[:MAX_INSIGHT_CHARS] or None
        category = article.source_category
        if category == "engineering":
            article.ai_summary = insight
        elif category == "strategy":
            article.first_principle = insight
        elif category == "pm":
            article.key_insight = insight
        elif category == "ai":
            article.ai_insight = insight

        return True

    def _call_claude(self, prompt: str) -> Optional[str]:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=settings.anthropic_api_key)
            response = client.messages.create(
                model=settings.anthropic_model,
                max_tokens=300,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except Exception as exc:
            logger.error("Claude API call failed: %s", exc)
            return None


ai_processing_service = AIProcessingService()
```

Commit: `Layer2 Step 5: add AIProcessingService with scoring and category insights`

---

### Step 6 — Wire AI processing into startup and background loop

File: `code/app/main.py`

**6a. Add import** at the top with other service imports:

```python
from app.services.ai_processing_service import ai_processing_service
```

**6b. Update startup fetch** — replace the existing startup block:

```python
    # Feed: initial fetch + AI processing
    db = SessionLocal()
    try:
        feed_service.fetch_all(db)
        ai_processing_service.process_unprocessed(db)
    finally:
        db.close()
```

**6c. Update background loop** — replace the existing `_refresh_loop`:

```python
    async def _refresh_loop():
        while True:
            await asyncio.sleep(6 * 3600)
            db = SessionLocal()
            try:
                feed_service.fetch_all(db)
                ai_processing_service.process_unprocessed(db)
            finally:
                db.close()
```

Commit: `Layer2 Step 6: wire AI processing into startup and background refresh`

---

### Step 7 — Update /api/feed/refresh to run AI processing

File: `code/app/routers/feed.py`

**7a. Add import** at the top:

```python
from app.services.ai_processing_service import ai_processing_service
```

**7b. Replace the existing refresh endpoint:**

```python
@router.post("/api/feed/refresh", response_class=JSONResponse)
async def refresh_feed(db: Session = Depends(get_db)):
    """Manually trigger a feed refresh and AI processing."""
    new_articles = feed_service.fetch_all(db)
    processed = ai_processing_service.process_unprocessed(db, limit=20)
    return {"status": "ok", "new_articles": new_articles, "ai_processed": processed}
```

Commit: `Layer2 Step 7: update /api/feed/refresh to include AI processing`

---

### Step 8 — Sort feed by AI score

File: `code/app/services/feed_service.py`

Replace the `get_articles` method with:

```python
    def get_articles(self, db: Session, category: str = "all", limit: int = 60) -> list[FeedArticle]:
        """Return feed articles sorted by AI score then date, optionally filtered by category."""
        query = db.query(FeedArticle).filter(FeedArticle.is_dismissed == False)
        if category != "all":
            query = query.filter(FeedArticle.source_category == category)
        return (
            query.order_by(
                FeedArticle.ai_score.desc().nullslast(),
                FeedArticle.published_at.desc().nullslast(),
                FeedArticle.fetched_at.desc(),
            )
            .limit(limit)
            .all()
        )
```

Commit: `Layer2 Step 8: sort feed articles by ai_score desc, hide dismissed`

---

### Step 9 — Update public feed template to show AI insights and score

File: `code/app/templates/feed/index.html`

Replace the entire file with:

```html
<!-- feed/index.html -->
{% extends "base.html" %}

{% block title %}PM Intelligence Feed — fullstackpm.tech{% endblock %}

{% block content %}
<section style="padding: 4rem 0 2rem; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-5xl mx-auto px-6">
    <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--color-accent);margin-bottom:0.5rem;">
      The Full Stack PM
    </p>
    <h1 style="font-size:2rem;font-weight:800;letter-spacing:-0.02em;color:var(--color-text-primary);margin-bottom:0.5rem;">
      PM Intelligence Feed
    </h1>
    <p style="font-size:0.95rem;color:var(--color-text-secondary);">
      60+ PM, engineering, strategy, and AI sources — scored and distilled for PMs. Updated every 6 hours.
    </p>
  </div>
</section>

<section style="padding: 1.5rem 0; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-5xl mx-auto px-6">
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      {% for key, label in categories %}
      <a href="/feed?category={{ key }}"
         style="display:inline-block;padding:6px 16px;border-radius:999px;font-size:0.85rem;font-weight:600;text-decoration:none;border:1px solid {{ 'var(--color-accent)' if active_category == key else 'var(--color-border)' }};background-color:{{ 'var(--color-accent)' if active_category == key else 'transparent' }};color:{{ '#fff' if active_category == key else 'var(--color-text-secondary)' }};">
        {{ label }}
      </a>
      {% endfor %}
    </div>
  </div>
</section>

{% macro category_colors(cat) %}
  {% if cat == 'pm' %}
    bg: var(--color-blue-100); color: var(--color-blue-900);
  {% elif cat == 'engineering' %}
    bg: var(--color-success-100); color: var(--color-success-900);
  {% elif cat == 'ai' %}
    bg: #ede9fe; color: #5b21b6;
  {% else %}
    bg: var(--color-warning-100); color: var(--color-warning-900);
  {% endif %}
{% endmacro %}

{% macro category_badge(cat) %}
  {% if cat == 'pm' %}
    <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:999px;background-color:var(--color-blue-100);color:var(--color-blue-900);">PM</span>
  {% elif cat == 'engineering' %}
    <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:999px;background-color:var(--color-success-100);color:var(--color-success-900);">ENGINEERING</span>
  {% elif cat == 'ai' %}
    <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:999px;background-color:#ede9fe;color:#5b21b6;">AI</span>
  {% else %}
    <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:999px;background-color:var(--color-warning-100);color:var(--color-warning-900);">STRATEGY</span>
  {% endif %}
{% endmacro %}

{% macro ai_insight_block(article, large=false) %}
  {% set insight = article.ai_summary or article.first_principle or article.key_insight or article.ai_insight %}
  {% if insight %}
    {% set label = 'PM Take →' if article.source_category == 'engineering' else ('First Principle' if article.source_category == 'strategy' else ('Takeaway' if article.source_category == 'pm' else 'AI for PMs')) %}
    <div style="margin-top:{{ '14px' if large else '10px' }};padding-top:{{ '14px' if large else '10px' }};border-top:1px solid var(--color-border);">
      <p style="font-size:{{ '0.9rem' if large else '0.8rem' }};line-height:1.55;color:var(--color-text-secondary);">
        <strong style="color:var(--color-accent);">{{ label }}:</strong> {{ insight }}
      </p>
    </div>
  {% endif %}
{% endmacro %}

<section style="padding: 3rem 0;">
  <div class="max-w-5xl mx-auto px-6">
    {% if not articles %}
    <div style="color:var(--color-text-tertiary);text-align:center;padding:4rem 0;">
      Feed is loading — check back in a minute.
      <form action="/api/feed/refresh" method="post" style="display:inline;">
        <button type="submit" style="color:var(--color-accent);background:none;border:none;cursor:pointer;padding:0;font:inherit;">
          Refresh now
        </button>
      </form>
    </div>
    {% else %}

    {% set featured = articles[0] %}
    <a href="{{ featured.url }}" target="_blank" rel="noopener noreferrer"
       style="display:block;border:1px solid var(--color-border);border-radius:12px;padding:28px 32px;margin-bottom:2rem;text-decoration:none;"
       class="card-hover">
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:12px;flex-wrap:wrap;">
        {{ category_badge(featured.source_category) }}
        {% if featured.is_editors_pick %}
        <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:999px;background-color:#fef3c7;color:#92400e;">★ EDITOR'S PICK</span>
        {% endif %}
        {% if featured.ai_score %}
        <span style="font-size:11px;font-weight:700;padding:2px 8px;border-radius:6px;background-color:{{ '#dcfce7' if featured.ai_score >= 8 else ('#fef9c3' if featured.ai_score >= 5 else '#f3f4f6') }};color:{{ '#166534' if featured.ai_score >= 8 else ('#854d0e' if featured.ai_score >= 5 else '#374151') }};">
          {{ featured.ai_score }}/10
        </span>
        {% endif %}
        <span style="font-size:12px;color:var(--color-text-tertiary);">{{ featured.source_name }}</span>
        {% if featured.published_at %}
        <span style="font-size:12px;color:var(--color-text-tertiary);">· {{ featured.published_at.strftime('%b %d') }}</span>
        {% endif %}
      </div>
      <h2 style="font-size:1.4rem;font-weight:800;letter-spacing:-0.02em;color:var(--color-text-primary);margin-bottom:10px;line-height:1.3;">
        {{ featured.title }}
      </h2>
      {% if featured.excerpt %}
      <p style="font-size:0.95rem;line-height:1.6;color:var(--color-text-secondary);">{{ featured.excerpt }}</p>
      {% endif %}
      {{ ai_insight_block(featured, large=true) }}
    </a>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {% for article in articles[1:] %}
      <a href="{{ article.url }}" target="_blank" rel="noopener noreferrer"
         style="display:block;border:1px solid var(--color-border);border-radius:12px;padding:20px 24px;text-decoration:none;"
         class="card-hover">
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap;">
          {{ category_badge(article.source_category) }}
          {% if article.is_editors_pick %}
          <span style="font-size:9px;font-weight:700;padding:2px 6px;border-radius:999px;background-color:#fef3c7;color:#92400e;">★ PICK</span>
          {% endif %}
          {% if article.ai_score %}
          <span style="font-size:10px;font-weight:700;padding:1px 6px;border-radius:4px;background-color:{{ '#dcfce7' if article.ai_score >= 8 else ('#fef9c3' if article.ai_score >= 5 else '#f3f4f6') }};color:{{ '#166534' if article.ai_score >= 8 else ('#854d0e' if article.ai_score >= 5 else '#374151') }};">
            {{ article.ai_score }}/10
          </span>
          {% endif %}
          <span style="font-size:11px;color:var(--color-text-tertiary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            {{ article.source_name }}
          </span>
        </div>
        <h3 style="font-size:0.95rem;font-weight:700;line-height:1.4;color:var(--color-text-primary);margin-bottom:8px;">
          {{ article.title }}
        </h3>
        {% if article.excerpt %}
        <p style="font-size:0.85rem;line-height:1.5;color:var(--color-text-secondary);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;">
          {{ article.excerpt }}
        </p>
        {% endif %}
        {{ ai_insight_block(article) }}
        {% if article.published_at %}
        <p style="font-size:11px;color:var(--color-text-tertiary);margin-top:12px;">
          {{ article.published_at.strftime('%b %d, %Y') }}
        </p>
        {% endif %}
      </a>
      {% endfor %}
    </div>
    {% endif %}
  </div>
</section>
{% endblock %}
```

Commit: `Layer2 Step 9: update feed template with AI insights, score badges, category colors`

---

### Step 10 — Add editorial routes to feed router

File: `code/app/routers/feed.py`

Replace the entire file with:

```python
# app/routers/feed.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.feed_article import FeedArticle
from app.services.feed_service import feed_service
from app.services.ai_processing_service import ai_processing_service

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

CATEGORIES = [
    ("all", "All"),
    ("pm", "Product"),
    ("engineering", "Engineering"),
    ("strategy", "Strategy"),
    ("ai", "AI & Research"),
]


def _check_editorial_token(token: str):
    if not token or token != settings.editorial_token:
        raise HTTPException(status_code=403, detail="Invalid editorial token")


@router.get("/feed", response_class=HTMLResponse)
async def feed_page(request: Request, category: str = "all", db: Session = Depends(get_db)):
    articles = feed_service.get_articles(db, category=category)
    return templates.TemplateResponse(
        "feed/index.html",
        {
            "request": request,
            "config": settings,
            "year": datetime.now().year,
            "title": "PM Intelligence Feed — fullstackpm.tech",
            "current_page": "/feed",
            "articles": articles,
            "active_category": category,
            "categories": CATEGORIES,
        },
    )


@router.get("/feed/editorial", response_class=HTMLResponse)
async def editorial_page(request: Request, token: str = "", db: Session = Depends(get_db)):
    """Editorial dashboard — token-gated."""
    _check_editorial_token(token)
    articles = (
        db.query(FeedArticle)
        .filter(FeedArticle.is_dismissed == False)
        .order_by(
            FeedArticle.is_editors_pick.desc(),
            FeedArticle.ai_score.desc().nullslast(),
            FeedArticle.fetched_at.desc(),
        )
        .limit(100)
        .all()
    )
    total = db.query(FeedArticle).count()
    processed = db.query(FeedArticle).filter(FeedArticle.ai_processed_at.isnot(None)).count()
    picks = db.query(FeedArticle).filter(FeedArticle.is_editors_pick == True).count()
    return templates.TemplateResponse(
        "feed/editorial.html",
        {
            "request": request,
            "config": settings,
            "year": datetime.now().year,
            "title": "Editorial Dashboard — fullstackpm.tech",
            "current_page": "/feed/editorial",
            "articles": articles,
            "token": token,
            "stats": {"total": total, "processed": processed, "picks": picks},
        },
    )


@router.post("/api/feed/refresh", response_class=JSONResponse)
async def refresh_feed(db: Session = Depends(get_db)):
    """Manually trigger a feed refresh and AI processing."""
    new_articles = feed_service.fetch_all(db)
    processed = ai_processing_service.process_unprocessed(db, limit=20)
    return {"status": "ok", "new_articles": new_articles, "ai_processed": processed}


@router.post("/api/feed/article/{article_id}/pick", response_class=HTMLResponse)
async def toggle_pick(article_id: int, token: str = "", db: Session = Depends(get_db)):
    """Toggle is_editors_pick. Returns updated button HTML for HTMX swap."""
    _check_editorial_token(token)
    article = db.query(FeedArticle).filter(FeedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_editors_pick = not article.is_editors_pick
    db.commit()
    label = "★ Featured" if article.is_editors_pick else "☆ Feature It"
    color = "var(--color-accent)" if article.is_editors_pick else "var(--color-text-tertiary)"
    return HTMLResponse(
        f'<button hx-post="/api/feed/article/{article_id}/pick?token={token}" '
        f'hx-target="this" hx-swap="outerHTML" '
        f'style="background:none;border:1px solid {color};color:{color};padding:4px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem;font-weight:600;">'
        f"{label}</button>"
    )


@router.post("/api/feed/article/{article_id}/dismiss", response_class=HTMLResponse)
async def dismiss_article(article_id: int, token: str = "", db: Session = Depends(get_db)):
    """Mark article as dismissed. Returns empty string to remove card from HTMX view."""
    _check_editorial_token(token)
    article = db.query(FeedArticle).filter(FeedArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article.is_dismissed = True
    db.commit()
    return HTMLResponse("")
```

Commit: `Layer2 Step 10: add editorial routes (dashboard, pick, dismiss)`

---

### Step 11 — Create editorial template

File: `code/app/templates/feed/editorial.html` (new file)

```html
<!-- feed/editorial.html -->
{% extends "base.html" %}

{% block title %}Editorial Dashboard — fullstackpm.tech{% endblock %}

{% block content %}
<section style="padding: 3rem 0 1.5rem; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-5xl mx-auto px-6">
    <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--color-accent);margin-bottom:0.5rem;">
      EDITORIAL
    </p>
    <h1 style="font-size:1.8rem;font-weight:800;letter-spacing:-0.02em;color:var(--color-text-primary);margin-bottom:1rem;">
      Feed Dashboard
    </h1>
    <div style="display:flex;gap:24px;flex-wrap:wrap;">
      <span style="font-size:0.85rem;color:var(--color-text-secondary);">
        <strong style="color:var(--color-text-primary);">{{ stats.total }}</strong> total articles
      </span>
      <span style="font-size:0.85rem;color:var(--color-text-secondary);">
        <strong style="color:var(--color-text-primary);">{{ stats.processed }}</strong> AI-processed
      </span>
      <span style="font-size:0.85rem;color:var(--color-text-secondary);">
        <strong style="color:var(--color-accent);">{{ stats.picks }}</strong> editor's picks
      </span>
      <form action="/api/feed/refresh" method="post" style="display:inline;">
        <button type="submit"
                style="background:none;border:1px solid var(--color-border);color:var(--color-text-secondary);padding:4px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;">
          ↻ Refresh feed
        </button>
      </form>
    </div>
  </div>
</section>

<section style="padding: 2rem 0;">
  <div class="max-w-5xl mx-auto px-6">
    {% if not articles %}
    <p style="color:var(--color-text-tertiary);text-align:center;padding:4rem 0;">No articles yet.</p>
    {% else %}
    <div style="display:flex;flex-direction:column;gap:1rem;">
      {% for article in articles %}
      <div id="article-{{ article.id }}"
           style="border:1px solid {{ 'var(--color-accent)' if article.is_editors_pick else 'var(--color-border)' }};border-radius:10px;padding:18px 22px;display:flex;gap:16px;align-items:flex-start;">

        <!-- Score column -->
        <div style="min-width:48px;text-align:center;">
          {% if article.ai_score %}
          <div style="font-size:1.1rem;font-weight:800;color:{{ '#16a34a' if article.ai_score >= 8 else ('#d97706' if article.ai_score >= 5 else '#9ca3af') }};">
            {{ article.ai_score }}
          </div>
          <div style="font-size:10px;color:var(--color-text-tertiary);">/10</div>
          {% else %}
          <div style="font-size:0.75rem;color:var(--color-text-tertiary);">–</div>
          {% endif %}
        </div>

        <!-- Content column -->
        <div style="flex:1;min-width:0;">
          <div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap;">
            <!-- Category badge -->
            {% if article.source_category == 'pm' %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background-color:var(--color-blue-100);color:var(--color-blue-900);">PM</span>
            {% elif article.source_category == 'engineering' %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background-color:var(--color-success-100);color:var(--color-success-900);">ENG</span>
            {% elif article.source_category == 'ai' %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background-color:#ede9fe;color:#5b21b6;">AI</span>
            {% else %}
            <span style="font-size:9px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:2px 8px;border-radius:999px;background-color:var(--color-warning-100);color:var(--color-warning-900);">STRATEGY</span>
            {% endif %}
            <span style="font-size:11px;color:var(--color-text-tertiary);">{{ article.source_name }}</span>
            {% if article.published_at %}
            <span style="font-size:11px;color:var(--color-text-tertiary);">· {{ article.published_at.strftime('%b %d') }}</span>
            {% endif %}
          </div>

          <a href="{{ article.url }}" target="_blank" rel="noopener noreferrer"
             style="font-size:0.95rem;font-weight:700;color:var(--color-text-primary);text-decoration:none;line-height:1.4;display:block;margin-bottom:6px;">
            {{ article.title }}
          </a>

          {% if article.ai_score_reason %}
          <p style="font-size:0.8rem;color:var(--color-text-tertiary);margin-bottom:6px;font-style:italic;">
            {{ article.ai_score_reason }}
          </p>
          {% endif %}

          {% set insight = article.ai_summary or article.first_principle or article.key_insight or article.ai_insight %}
          {% if insight %}
          {% set label = 'PM Take' if article.source_category == 'engineering' else ('First Principle' if article.source_category == 'strategy' else ('Takeaway' if article.source_category == 'pm' else 'AI for PMs')) %}
          <p style="font-size:0.85rem;line-height:1.5;color:var(--color-text-secondary);">
            <strong style="color:var(--color-accent);">{{ label }}:</strong> {{ insight }}
          </p>
          {% endif %}

          <!-- Actions -->
          <div style="display:flex;gap:8px;margin-top:12px;align-items:center;">
            {{ toggle_pick_button(article) }}
            <button hx-post="/api/feed/article/{{ article.id }}/dismiss?token={{ token }}"
                    hx-target="#article-{{ article.id }}"
                    hx-swap="outerHTML"
                    style="background:none;border:1px solid var(--color-border);color:var(--color-text-tertiary);padding:4px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem;">
              → Skip
            </button>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
    {% endif %}
  </div>
</section>

{% macro toggle_pick_button(article) %}
<button hx-post="/api/feed/article/{{ article.id }}/pick?token={{ token }}"
        hx-target="this"
        hx-swap="outerHTML"
        style="background:none;border:1px solid {{ 'var(--color-accent)' if article.is_editors_pick else 'var(--color-text-tertiary)' }};color:{{ 'var(--color-accent)' if article.is_editors_pick else 'var(--color-text-tertiary)' }};padding:4px 12px;border-radius:6px;cursor:pointer;font-size:0.8rem;font-weight:600;">
  {{ '★ Featured' if article.is_editors_pick else '☆ Feature It' }}
</button>
{% endmacro %}

<script src="https://unpkg.com/htmx.org@1.9.10"></script>
{% endblock %}
```

Commit: `Layer2 Step 11: add editorial dashboard template`

---

### Step 12 — Push and verify

```bash
git push origin main
```

After Render deploys (~2 min):

1. Visit `https://fullstackpm.tech/feed` — articles should appear with score badges and AI insights (initially empty if not yet processed; trigger `/api/feed/refresh` via curl or browser POST)
2. Visit `https://fullstackpm.tech/feed/editorial?token=fspm-editorial-2026` — editorial dashboard should load
3. Confirm ANTHROPIC_API_KEY is set in Render env vars (Settings → Environment)
4. Confirm EDITORIAL_TOKEN is set (or use the default `fspm-editorial-2026`)
5. Trigger a manual refresh from the editorial dashboard and check that AI processing runs in Render logs

Commit: N/A (just a push)

---

## Results (fill in after completing)

| Step | Status | Notes |
|------|--------|-------|
| 1 — Add anthropic to requirements.txt | done | Added `anthropic>=0.40.0`; committed `b4a5c06`. |
| 2 — Config keys | done | Added `anthropic_api_key`, `anthropic_model`, and `editorial_token`; committed `c4b7844`. |
| 3 — Model + migration | done | Extended `FeedArticle` with Layer 2 fields and added `ensure_feed_layer2_columns()`; committed `2e62e7c`. |
| 4 — Wire migration in startup | done | Startup now runs `init_db()` then `ensure_feed_layer2_columns()`; committed `9b985b2`. |
| 5 — AIProcessingService | done | Added Claude Haiku scoring/insight service with JSON parsing and score clamping; committed `5f2a6b2`. |
| 6 — Wire AI processing in refresh loops | done | Startup fetch and 6-hour background refresh now run AI processing; committed `83f4f22`. |
| 7 — Update /api/feed/refresh | done | Manual refresh now returns `new_articles` and `ai_processed`; committed `248a9df`. |
| 8 — Sort by ai_score | done | Public feed hides dismissed articles and sorts by AI score/date; committed `2192d90`. |
| 9 — Update public feed template | done | Public feed now supports score badges, editor picks, and category insights; committed `ba8e44f`. |
| 10 — Editorial routes | done | Added token-gated dashboard plus pick/dismiss HTMX endpoints; committed `96f6786`. |
| 11 — Editorial template | done | Added editorial dashboard template; committed `1838297`. |
| 12 — Push + verify | done | Pushed to `main`; live `/feed` = 200, `/feed/editorial?token=fspm-editorial-2026` = 200, bad token = 403, refresh = 200. Live refresh returned `ai_processed: 0`; Render likely still needs `ANTHROPIC_API_KEY` set. Confirm `EDITORIAL_TOKEN` too if overriding default. |

---

## Blockers reference

- **`anthropic` ImportError on startup**: `anthropic` not in requirements.txt — check Step 1.
- **403 on editorial page**: token mismatch — confirm `EDITORIAL_TOKEN` env var on Render matches what you're passing.
- **AI processing not running**: `ANTHROPIC_API_KEY` not set in Render env — check the service logs for the warning message.
- **Migration fails**: `feed_articles` table locked — restart the Render service to release the lock.
- **HTMX buttons not working**: verify `htmx.org` script tag loads in editorial.html (Step 11 includes it).
