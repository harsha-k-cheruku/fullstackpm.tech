# PM Intelligence Feed — Layer 2 Build Plan

**Created:** 2026-06-01
**Depends on:** Layer 1 live at `https://fullstackpm.tech/feed`
**Scope:** Planning only. Do not build until owner approves open questions.

---

## Goal

Layer 1 stores and displays raw RSS articles. Layer 2 adds lightweight AI processing so each article card gives a PM-readable reason to care:

- Engineering posts get a PM-lens summary.
- Strategy posts get a first-principles / mental-model extraction.
- PM posts get one actionable takeaway.

No personalization, accounts, editor UI, ranking changes, or new RSS sources in this layer.

---

## 1. Exact SQLAlchemy model changes

File: `code/app/models/feed_article.py`

Add the three display/output fields requested by scope:

```python
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

class FeedArticle(Base):
    __tablename__ = "feed_articles"

    # existing Layer 1 fields...
    ai_summary = Column(Text, nullable=True)       # Engineering: PM-lens explanation
    first_principle = Column(Text, nullable=True)  # Strategy: mental model / first-principles extraction
    key_insight = Column(Text, nullable=True)      # PM: single actionable insight
```

Recommended additional operational field:

```python
ai_processed_at = Column(DateTime, nullable=True)  # Timestamp used to identify unprocessed rows
```

Why this fourth field matters: the Layer 2 scope says processing should query rows where `ai_processed_at IS NULL`, mark completed rows with the current timestamp, and avoid repeatedly processing the same article. Without it, the service has to infer state from three nullable output columns, which is brittle and category-dependent.

### SQLite migration approach

Because `init_db()` only creates missing tables and does not alter existing tables, add a tiny idempotent migration helper or run manual SQL once in Render shell:

```sql
ALTER TABLE feed_articles ADD COLUMN ai_summary TEXT;
ALTER TABLE feed_articles ADD COLUMN first_principle TEXT;
ALTER TABLE feed_articles ADD COLUMN key_insight TEXT;
ALTER TABLE feed_articles ADD COLUMN ai_processed_at DATETIME;
```

SQLite does not support `ADD COLUMN IF NOT EXISTS` on all deployed versions, so preferred app-side helper should inspect existing columns first:

```python
from sqlalchemy import inspect, text


def ensure_feed_layer2_columns(engine) -> None:
    existing = {col["name"] for col in inspect(engine).get_columns("feed_articles")}
    statements = {
        "ai_summary": "ALTER TABLE feed_articles ADD COLUMN ai_summary TEXT",
        "first_principle": "ALTER TABLE feed_articles ADD COLUMN first_principle TEXT",
        "key_insight": "ALTER TABLE feed_articles ADD COLUMN key_insight TEXT",
        "ai_processed_at": "ALTER TABLE feed_articles ADD COLUMN ai_processed_at DATETIME",
    }
    with engine.begin() as conn:
        for column, statement in statements.items():
            if column not in existing:
                conn.execute(text(statement))
```

Call this after `init_db()` in `lifespan()` before any feed fetch/processing runs.

---

## 2. `AIProcessingService` skeleton

File: `code/app/services/ai_processing_service.py`

```python
# app/services/ai_processing_service.py
from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.feed_article import FeedArticle

logger = logging.getLogger(__name__)

MAX_ARTICLES_PER_RUN = 20
MODEL_NAME = "claude-haiku-4-5-20251001"


class AIProcessingService:
    """AI enrichment pipeline for PM Intelligence Feed articles.

    Layer 2 processes raw Layer 1 RSS articles into category-specific PM-facing
    annotations. It is intentionally best-effort: failures are logged and skipped
    so feed fetching/display never breaks because an LLM call failed.
    """

    def process_unprocessed(self, db: Session, limit: int = MAX_ARTICLES_PER_RUN) -> int:
        """Process unprocessed articles and return the number successfully enriched.

        Selects `FeedArticle` rows where `ai_processed_at IS NULL`, ordered newest
        first, capped by `limit`. For each article, routes to the category-specific
        processor, writes exactly one output field, and sets `ai_processed_at`.
        """
        raise NotImplementedError

    def process_article(self, article: FeedArticle) -> bool:
        """Process one article based on `source_category`.

        Returns True if processing succeeded and article fields were updated.
        Returns False for unsupported categories or empty model output.
        """
        raise NotImplementedError

    def _process_engineering(self, article: FeedArticle) -> Optional[str]:
        """Return a PM-lens summary for an engineering article.

        Prompt goal: explain what changed, why the engineering team made the
        decision, and what PMs should understand about the trade-off in under
        100 words.
        """
        raise NotImplementedError

    def _process_strategy(self, article: FeedArticle) -> Optional[str]:
        """Return a first-principles insight for a strategy article.

        Prompt goal: one sentence with the core insight plus the mental model it
        illustrates, e.g. network effects, switching costs, regulatory capture.
        """
        raise NotImplementedError

    def _process_pm(self, article: FeedArticle) -> Optional[str]:
        """Return one actionable takeaway for a PM article.

        Prompt goal: one sentence describing the single most actionable insight
        for a practising PM.
        """
        raise NotImplementedError

    def _call_claude(self, prompt: str) -> Optional[str]:
        """Call Claude Haiku using `ANTHROPIC_API_KEY` and return stripped text.

        This method owns Anthropic SDK details, timeout handling, logging, and
        empty-response normalization. It should not raise for normal API errors.
        """
        raise NotImplementedError


ai_processing_service = AIProcessingService()
```

### Implementation notes

- Use `ANTHROPIC_API_KEY` from environment.
- Use Claude Haiku model from scope: `claude-haiku-4-5-20251001`.
- Include article title, source, excerpt, and URL in prompts.
- Do not fetch full article bodies in Layer 2 unless explicitly approved; use stored RSS title/excerpt to keep implementation small and cheap.
- Log and skip failed articles. Do not block feed rendering.

---

## 3. Where it plugs into `FeedService.fetch_all()`

Current Layer 1 flow:

```python
feed_service.fetch_all(db)
```

Recommended Layer 2 flow:

```python
from app.services.ai_processing_service import ai_processing_service

new_count = feed_service.fetch_all(db)
ai_count = ai_processing_service.process_unprocessed(db, limit=20)
```

Plug-in points:

1. Startup fetch in `code/app/main.py` after `feed_service.fetch_all(db)`.
2. Six-hour background refresh loop after `feed_service.fetch_all(db)`.
3. Manual refresh route `/api/feed/refresh` after `feed_service.fetch_all(db)`, returning both counts:

```python
@router.post("/api/feed/refresh", response_class=JSONResponse)
async def refresh_feed(db: Session = Depends(get_db)):
    """Manually trigger a feed refresh and Layer 2 processing."""
    new_articles = feed_service.fetch_all(db)
    processed_articles = ai_processing_service.process_unprocessed(db, limit=20)
    return {
        "status": "ok",
        "new_articles": new_articles,
        "processed_articles": processed_articles,
    }
```

Keep `FeedService` focused on RSS persistence. Do not bury LLM calls inside the low-level RSS parsing loop. This separation keeps tests sane and prevents an LLM outage from making feed ingestion look broken.

---

## 4. Template snippets for article cards

File: `code/app/templates/feed/index.html`

### Featured card snippet

Place below featured excerpt:

```html
{% if featured.source_category == 'engineering' and featured.ai_summary %}
<div style="margin-top:14px;padding-top:14px;border-top:1px solid var(--color-border);">
  <p style="font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--color-accent);margin-bottom:6px;">
    PM Take →
  </p>
  <p style="font-size:0.9rem;line-height:1.55;color:var(--color-text-secondary);">
    {{ featured.ai_summary }}
  </p>
</div>
{% elif featured.source_category == 'strategy' and featured.first_principle %}
<p style="margin-top:14px;font-size:0.85rem;color:var(--color-text-secondary);">
  <strong style="color:var(--color-text-primary);">First principle:</strong>
  {{ featured.first_principle }}
</p>
{% elif featured.source_category == 'pm' and featured.key_insight %}
<p style="margin-top:14px;font-size:0.85rem;color:var(--color-text-secondary);">
  <strong style="color:var(--color-text-primary);">Takeaway:</strong>
  {{ featured.key_insight }}
</p>
{% endif %}
```

### Grid card snippet

Place below each card excerpt:

```html
{% if article.source_category == 'engineering' and article.ai_summary %}
<p style="margin-top:10px;font-size:0.8rem;line-height:1.45;color:var(--color-text-secondary);border-top:1px solid var(--color-border);padding-top:10px;">
  <strong style="color:var(--color-accent);">PM Take →</strong>
  {{ article.ai_summary }}
</p>
{% elif article.source_category == 'strategy' and article.first_principle %}
<p style="margin-top:10px;font-size:0.8rem;line-height:1.45;color:var(--color-text-secondary);">
  <strong style="color:var(--color-text-primary);">First principle:</strong>
  {{ article.first_principle }}
</p>
{% elif article.source_category == 'pm' and article.key_insight %}
<p style="margin-top:10px;font-size:0.8rem;line-height:1.45;color:var(--color-text-secondary);">
  <strong style="color:var(--color-text-primary);">Takeaway:</strong>
  {{ article.key_insight }}
</p>
{% endif %}
```

Unprocessed articles should continue to render the raw excerpt only. No placeholder is needed unless owner wants explicit processing state.

---

## 5. Suggested build sequence

1. Add model columns and migration helper.
2. Add `AIProcessingService` with prompts and Anthropic SDK wrapper.
3. Add unit tests for routing logic without calling Anthropic.
4. Wire processing after startup/background/manual feed refresh.
5. Update feed template with conditional snippets.
6. Run local smoke test against a handful of existing articles.
7. Push and verify Render logs plus `/feed` rendering.

---

## 6. Effort estimate

Estimated implementation time: **4–6 hours**.

Breakdown:

- Model + migration helper: 0.75 hour
- AI service + prompts + Anthropic integration: 1.5–2 hours
- Wiring into startup/background/manual refresh: 0.5 hour
- Template updates: 0.75 hour
- Tests/smoke verification/log review: 1–2 hours

---

## 7. Open questions before building

1. The handoff asks for "3 new columns," but the scope doc also requires `ai_processed_at` for processing state. Should Layer 2 add the timestamp column too? Recommendation: yes.
2. Should Layer 2 use only RSS title/excerpt, or should it fetch full article HTML before prompting? Recommendation: RSS only for v1 to keep cost/latency low.
3. Should processing happen synchronously after fetch, or in a separate background task/queue? Recommendation: synchronous after fetch with a hard limit of 20 articles per run for v1.
4. Should failed articles be retried later? Recommendation: add `ai_processing_error` only in a later layer if failures become noisy; for v1, log and leave `ai_processed_at` null.
5. Should unprocessed cards show a "processing..." placeholder? Recommendation: no. Raw excerpt is enough and avoids UI noise.
6. Should PM/strategy outputs be one sentence max enforced in prompt only, or truncated in code? Recommendation: prompt plus a conservative character cap before saving.
