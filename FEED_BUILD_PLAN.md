# PM Intelligence Feed — Layer 1 Build Plan

**Created:** 2026-05-31
**Status:** Ready to execute.
**Assigned to:** Code Puppy
**Validate after:** Tomorrow morning — read this file and check the live site.

---

## What we're building

A `/feed` page that aggregates PM, engineering, and strategy content from 20+ RSS sources into a newspaper-style layout. Think Techmeme but for product people.

**This sprint (Layer 1):** Fetch → store → display. No AI processing yet.
**Layer 2 (future):** AI distillation of engineering posts into PM-lens summaries.

---

## What NOT to build in this sprint

- No AI summarization (that's Layer 2)
- No user accounts or personalization
- No admin UI for managing sources
- Do not touch the homepage (`index.html`) — build `/feed` as a new page
- Do not remove or modify any existing routers or services

---

## Architecture overview

```
RSS sources (20+)
      ↓
FeedService.fetch_all()  ←  runs at startup + every 6h via background task
      ↓
FeedArticle (SQLite)  ←  deduped by URL
      ↓
/feed route  →  feed/index.html template  →  newspaper layout
```

---

## Step 1 — Database model

**File:** `code/app/models/feed_article.py`

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
    source_category = Column(String(50), nullable=False)  # 'pm' | 'engineering' | 'strategy'
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    is_editors_pick = Column(Boolean, default=False)
```

Register the model in `code/app/models/__init__.py` — add the import line and add `FeedArticle` to `__all__`.

Also add the import in `code/app/main.py` alongside the other model imports so `init_db()` creates the table:
```python
from app.models.feed_article import FeedArticle  # noqa: F401
```

---

## Step 2 — Feed sources config

**File:** `code/app/services/feed_sources.py`

Create this file with the full source list:

```python
# app/services/feed_sources.py
FEED_SOURCES = [
    # ── PM & Product ──────────────────────────────────────────────
    {"name": "Lenny's Newsletter",       "url": "https://www.lennysnewsletter.com/feed",              "category": "pm"},
    {"name": "Product Talk",             "url": "https://www.producttalk.org/feed/",                   "category": "pm"},
    {"name": "Mind the Product",         "url": "https://www.mindtheproduct.com/feed/",                "category": "pm"},
    {"name": "Silicon Valley PG",        "url": "https://svpg.com/feed/",                              "category": "pm"},
    {"name": "Product Coalition",        "url": "https://medium.com/feed/product-coalition",           "category": "pm"},
    {"name": "Productboard Blog",        "url": "https://www.productboard.com/blog/feed/",             "category": "pm"},
    {"name": "Intercom Blog",            "url": "https://www.intercom.com/blog/feed",                  "category": "pm"},
    {"name": "Amplitude Blog",           "url": "https://amplitude.com/blog/feed",                     "category": "pm"},

    # ── Engineering (for PM lens in Layer 2) ──────────────────────
    {"name": "Netflix Tech Blog",        "url": "https://netflixtechblog.com/feed",                    "category": "engineering"},
    {"name": "Google Engineering",       "url": "https://engineering.googleblog.com/feeds/posts/default", "category": "engineering"},
    {"name": "Meta Engineering",         "url": "https://engineering.fb.com/feed/",                    "category": "engineering"},
    {"name": "AWS Blog",                 "url": "https://aws.amazon.com/blogs/aws/feed/",              "category": "engineering"},
    {"name": "Martin Fowler",            "url": "https://martinfowler.com/feed.atom",                  "category": "engineering"},
    {"name": "The Pragmatic Engineer",   "url": "https://newsletter.pragmaticengineer.com/feed",       "category": "engineering"},
    {"name": "Uber Engineering",         "url": "https://www.uber.com/en-US/blog/engineering/rss/",    "category": "engineering"},

    # ── Strategy & Business ───────────────────────────────────────
    {"name": "First Round Review",       "url": "https://review.firstround.com/feed.xml",              "category": "strategy"},
    {"name": "a16z",                     "url": "https://a16z.com/feed/",                              "category": "strategy"},
    {"name": "Benedict Evans",           "url": "https://www.ben-evans.com/benedictevans/rss.xml",     "category": "strategy"},
    {"name": "HBR",                      "url": "https://feeds.hbr.org/harvardbusiness",               "category": "strategy"},
    {"name": "Reforge Blog",             "url": "https://www.reforge.com/blog/rss",                    "category": "strategy"},
]
```

---

## Step 3 — FeedService

**File:** `code/app/services/feed_service.py`

This extends the existing `ReadingService` pattern but writes to SQLite for persistence.

```python
# app/services/feed_service.py
from __future__ import annotations

import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional

import feedparser
from sqlalchemy.orm import Session

from app.models.feed_article import FeedArticle
from app.services.feed_sources import FEED_SOURCES

logger = logging.getLogger(__name__)

MAX_ARTICLES_PER_SOURCE = 5
MAX_EXCERPT_CHARS = 300


def _parse_date(entry) -> Optional[datetime]:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                import time
                return datetime(*val[:6])
            except Exception:
                pass
    return None


def _clean_excerpt(entry) -> str:
    raw = entry.get("summary", "") or entry.get("content", [{}])[0].get("value", "")
    # Strip HTML tags simply
    import re
    text = re.sub(r"<[^>]+>", " ", raw)
    text = " ".join(text.split())
    return text[:MAX_EXCERPT_CHARS].rstrip() + ("…" if len(text) > MAX_EXCERPT_CHARS else "")


class FeedService:
    def fetch_all(self, db: Session) -> int:
        """Fetch all RSS sources and upsert into DB. Returns count of new articles."""
        new_count = 0
        for source in FEED_SOURCES:
            try:
                feed = feedparser.parse(source["url"])
                for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
                    url = entry.get("link", "").strip()
                    if not url:
                        continue
                    exists = db.query(FeedArticle).filter_by(url=url).first()
                    if exists:
                        continue
                    article = FeedArticle(
                        title=entry.get("title", "Untitled")[:500],
                        url=url,
                        excerpt=_clean_excerpt(entry),
                        source_name=source["name"],
                        source_category=source["category"],
                        published_at=_parse_date(entry),
                    )
                    db.add(article)
                    new_count += 1
                db.commit()
            except Exception as e:
                logger.warning(f"Feed fetch failed for {source['name']}: {e}")
                db.rollback()
        return new_count

    def get_articles(self, db: Session, category: str = "all", limit: int = 60) -> list[FeedArticle]:
        q = db.query(FeedArticle)
        if category != "all":
            q = q.filter(FeedArticle.source_category == category)
        return q.order_by(FeedArticle.published_at.desc().nullslast(), FeedArticle.fetched_at.desc()).limit(limit).all()


feed_service = FeedService()
```

---

## Step 4 — Router

**File:** `code/app/routers/feed.py`

```python
# app/routers/feed.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.services.feed_service import feed_service

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("/feed", response_class=HTMLResponse)
async def feed_page(request: Request, category: str = "all", db: Session = Depends(get_db)):
    articles = feed_service.get_articles(db, category=category)
    return templates.TemplateResponse("feed/index.html", {
        "request": request,
        "title": "PM Intelligence Feed — fullstackpm.tech",
        "articles": articles,
        "active_category": category,
        "categories": [
            ("all", "All"),
            ("pm", "Product"),
            ("engineering", "Engineering"),
            ("strategy", "Strategy"),
        ],
    })


@router.post("/api/feed/refresh", response_class=JSONResponse)
async def refresh_feed(db: Session = Depends(get_db)):
    """Manually trigger a feed refresh."""
    count = feed_service.fetch_all(db)
    return {"status": "ok", "new_articles": count}
```

Register in `code/app/main.py`:
```python
from app.routers import feed
# ...
app.include_router(feed.router)
```

---

## Step 5 — Startup + background refresh

In `code/app/main.py`, update the `lifespan` function to fetch feeds at startup and schedule periodic refresh:

```python
from app.database import SessionLocal
from app.services.feed_service import feed_service
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # ... existing content_service and reading_service setup ...

    # Feed: initial fetch
    db = SessionLocal()
    try:
        feed_service.fetch_all(db)
    finally:
        db.close()

    # Feed: background refresh every 6 hours
    async def _refresh_loop():
        while True:
            await asyncio.sleep(6 * 3600)
            db = SessionLocal()
            try:
                feed_service.fetch_all(db)
            finally:
                db.close()

    task = asyncio.create_task(_refresh_loop())
    yield
    task.cancel()
```

---

## Step 6 — Template

**File:** `code/app/templates/feed/index.html`

Create the directory `code/app/templates/feed/` and this file:

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
      Curated from 20+ PM, engineering, and strategy sources. Updated every 6 hours.
    </p>
  </div>
</section>

<!-- Category filter tabs -->
<section style="padding: 1.5rem 0; border-bottom: 1px solid var(--color-border);">
  <div class="max-w-5xl mx-auto px-6">
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      {% for key, label in categories %}
      <a href="/feed?category={{ key }}"
         style="display:inline-block;padding:6px 16px;border-radius:999px;font-size:0.85rem;font-weight:600;text-decoration:none;
                border: 1px solid {{ 'var(--color-accent)' if active_category == key else 'var(--color-border)' }};
                background-color: {{ 'var(--color-accent)' if active_category == key else 'transparent' }};
                color: {{ '#fff' if active_category == key else 'var(--color-text-secondary)' }};">
        {{ label }}
      </a>
      {% endfor %}
    </div>
  </div>
</section>

<!-- Article grid -->
<section style="padding: 3rem 0;">
  <div class="max-w-5xl mx-auto px-6">
    {% if not articles %}
    <p style="color:var(--color-text-tertiary);text-align:center;padding:4rem 0;">
      Feed is loading — check back in a minute.
      <a href="/api/feed/refresh" style="color:var(--color-accent);">Refresh now</a>
    </p>
    {% else %}

    <!-- Featured: first article full-width -->
    {% set featured = articles[0] %}
    <a href="{{ featured.url }}" target="_blank" rel="noopener noreferrer"
       style="display:block;border:1px solid var(--color-border);border-radius:12px;padding:28px 32px;margin-bottom:2rem;text-decoration:none;"
       class="card-hover">
      <div style="display:flex;gap:10px;align-items:center;margin-bottom:12px;">
        <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
                     padding:3px 10px;border-radius:999px;
                     background-color:{{ 'var(--color-blue-100)' if featured.source_category == 'pm' else ('var(--color-success-100)' if featured.source_category == 'engineering' else 'var(--color-warning-100)') }};
                     color:{{ 'var(--color-blue-900)' if featured.source_category == 'pm' else ('var(--color-success-900)' if featured.source_category == 'engineering' else 'var(--color-warning-900)') }};">
          {{ featured.source_category | upper }}
        </span>
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
    </a>

    <!-- Grid: remaining articles -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {% for article in articles[1:] %}
      <a href="{{ article.url }}" target="_blank" rel="noopener noreferrer"
         style="display:block;border:1px solid var(--color-border);border-radius:12px;padding:20px 24px;text-decoration:none;"
         class="card-hover">
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;">
          <span style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
                       padding:2px 8px;border-radius:999px;
                       background-color:{{ 'var(--color-blue-100)' if article.source_category == 'pm' else ('var(--color-success-100)' if article.source_category == 'engineering' else 'var(--color-warning-100)') }};
                       color:{{ 'var(--color-blue-900)' if article.source_category == 'pm' else ('var(--color-success-900)' if article.source_category == 'engineering' else 'var(--color-warning-900)') }};">
            {{ article.source_category | upper }}
          </span>
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

---

## Step 7 — Add "Feed" to navigation

**File:** `code/app/templates/partials/navbar.html`

In the `nav_links` list, add `("Feed", "/feed")` after `("Blog", "/blog")`:

```python
{% set nav_links = [
  ("Home", "/"),
  ("Projects", "/projects"),
  ("Blog", "/blog"),
  ("Feed", "/feed"),
  ("Newsletter", "https://app.kit.com/forms/9506742/subscriptions"),
  ("Podcasts", "/resources"),
  ("@fullstackpm", "/@fullstackpm"),
] %}
```

Also add it to the footer quick links in `code/app/templates/partials/footer.html`.

---

## Verify checklist

After completing all steps, push to main and verify:

- [ ] `https://fullstackpm.tech/feed` loads without error
- [ ] Articles appear from multiple sources
- [ ] Category filter tabs work (PM / Engineering / Strategy)
- [ ] Each card links to the original article (opens in new tab)
- [ ] Featured (first) article renders larger/full-width
- [ ] "Feed" appears in navbar and footer
- [ ] `POST /api/feed/refresh` returns `{"status": "ok", "new_articles": N}`
- [ ] No errors in Render logs at startup

## If a feed URL 404s or times out

`FeedService.fetch_all()` silently skips broken sources — the rest will still load. Don't block on fixing individual source URLs.

---

*Layer 2 (AI distillation of engineering posts) will be a separate plan once Layer 1 is validated live.*
