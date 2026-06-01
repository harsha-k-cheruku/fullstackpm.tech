# app/services/feed_service.py
from __future__ import annotations

import logging
import re
from datetime import datetime
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
        value = getattr(entry, attr, None)
        if value:
            try:
                return datetime(*value[:6])
            except Exception:
                pass
    return None


def _clean_excerpt(entry) -> str:
    content = entry.get("content", [])
    raw = entry.get("summary", "")
    if not raw and content:
        raw = content[0].get("value", "")

    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = " ".join(text.split())
    if len(text) <= MAX_EXCERPT_CHARS:
        return text
    return text[:MAX_EXCERPT_CHARS].rstrip() + "…"


class FeedService:
    def fetch_all(self, db: Session) -> int:
        """Fetch all RSS sources and store new articles. Return new article count."""
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
            except Exception as exc:
                logger.warning("Feed fetch failed for %s: %s", source["name"], exc)
                db.rollback()
        return new_count

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


feed_service = FeedService()
