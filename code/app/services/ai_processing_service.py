# app/services/ai_processing_service.py
from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.models.feed_article import FeedArticle

logger = logging.getLogger(__name__)

MAX_ARTICLES_PER_RUN = 20
MAX_INSIGHT_CHARS = 400

_ANALYSIS_SYSTEM = """You are a senior PM analyst writing a deep read for product managers.

Given an article title and excerpt, write a 250-300 word analysis. No headers, no bullet points, no markdown — clean prose a PM can read in 90 seconds.

Structure depends on category:
- engineering: What changed and what it signals. Why it matters for product strategy — what decisions does this affect? The trade-off or risk — what breaks or gets harder? What a sharp PM should watch for next.
- strategy: The move and what it reveals. The first-principles mental model it illustrates (network effects, switching costs, platform dynamics, regulatory capture, flywheel, etc.). Competitive implications — who wins, who loses. One concrete thing worth tracking.
- pm: The core idea or framework. How to apply it — make it concrete. Where it breaks down or doesn't apply. One thing a PM should actually do differently after reading this.
- ai: What the capability or development is. The product opportunity it creates for B2B SaaS. The risk or limitation PMs need to plan around. What building with AI looks like differently because of this.

Write like you are briefing a smart peer, not teaching a student. Direct, specific, no filler. End with one sharp observation or question that makes the reader think."""

_SYSTEM_PROMPT = """You are a senior product manager analyst. Given an article title and excerpt, return a JSON object with exactly these keys:
- "title": a clean, specific 5-9 word headline that captures what the article is actually about. No episode numbers, no newsletter series names, no vague phrases. Write it like a newspaper headline — concrete noun + specific action or finding. Example: "DuckDB 1.0 Adds Persistent Storage Layer" not "Weekly Dose of Optimism #195"
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

        # Strip markdown code fences if Claude wraps JSON in ```json ... ```
        cleaned = raw.strip()
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
        if fence_match:
            cleaned = fence_match.group(1).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON from Claude for article %s: %s", article.id, raw[:200])
            return False

        raw_title = (data.get("title") or "").strip()
        if raw_title:
            article.display_title = raw_title[:300]

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

    def generate_article_analysis(self, article: FeedArticle, db: Session) -> Optional[str]:
        """Generate a 250-300 word deep analysis for the article page. Saves and returns the text."""
        if not settings.anthropic_api_key:
            return None
        prompt = (
            f"Category: {article.source_category}\n"
            f"Source: {article.source_name}\n"
            f"Title: {article.title}\n"
            f"Excerpt: {article.excerpt or '(no excerpt available — analyse based on title and source)'}\n\n"
            "Write the analysis now."
        )
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=settings.anthropic_api_key)
            response = client.messages.create(
                model=settings.anthropic_model,
                max_tokens=600,
                system=_ANALYSIS_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            analysis = response.content[0].text.strip()
            article.ai_article_analysis = analysis
            db.commit()
            return analysis
        except Exception as exc:
            logger.error("Article analysis generation failed for %s: %s", article.id, exc)
            db.rollback()
            return None

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
