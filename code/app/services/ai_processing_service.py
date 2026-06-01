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

        score = int(data.get("score", 0)) or None
        article.ai_score = max(1, min(score, 10)) if score else None
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
