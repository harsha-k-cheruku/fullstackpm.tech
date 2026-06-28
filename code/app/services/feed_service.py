# app/services/feed_service.py
from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import feedparser
from sqlalchemy.orm import Session

from app.models.feed_article import FeedArticle
from app.services.feed_sources import FEED_SOURCES

logger = logging.getLogger(__name__)

MAX_ARTICLES_PER_SOURCE = 5
MAX_EXCERPT_CHARS = 300

# Match emoji/pictograph Unicode ranges common in RSS feed titles
_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FFFF"
    "\U00002600-\U000027BF"
    "\U0000FE00-\U0000FE0F"
    "\U00002500-\U00002BFF]+",
    flags=re.UNICODE,
)


def _clean_title(text: str) -> str:
    return _EMOJI_RE.sub("", text).strip()


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
    def sync_from_json(self, db: Session, json_path: Path) -> int:
        """
        Upsert articles from the pre-processed articles.json into SQLite.
        Called on startup so the DB is always populated from the committed JSON.
        Preserves editorial overrides (is_editors_pick, is_dismissed) set via dashboard.
        """
        if not json_path.exists():
            return 0
        try:
            data = json.loads(json_path.read_text())
        except Exception as exc:
            logger.warning("Failed to load articles.json: %s", exc)
            return 0

        upserted = 0
        for a in data.get("articles", []):
            url = a.get("url", "").strip()
            if not url:
                continue
            try:
                existing = db.query(FeedArticle).filter_by(url=url).first()
                if existing:
                    # Update AI fields only — preserve editorial overrides
                    existing.title          = a.get("title") or existing.title
                    existing.display_title  = a.get("display_title")
                    existing.excerpt        = a.get("excerpt") or existing.excerpt
                    existing.ai_score       = a.get("ai_score")
                    existing.ai_score_reason = a.get("ai_score_reason")
                    existing.ai_summary     = a.get("ai_summary")
                    existing.first_principle = a.get("first_principle")
                    existing.key_insight    = a.get("key_insight")
                    existing.ai_insight     = a.get("ai_insight")
                    existing.ai_article_analysis = a.get("ai_article_analysis")
                else:
                    pub = a.get("published_at")
                    fetched = a.get("fetched_at")
                    db.add(FeedArticle(
                        url=url,
                        title=a.get("title", "")[:500],
                        display_title=a.get("display_title"),
                        excerpt=a.get("excerpt"),
                        source_name=a.get("source_name", ""),
                        source_category=a.get("source_category", ""),
                        published_at=datetime.fromisoformat(pub) if pub else None,
                        fetched_at=datetime.fromisoformat(fetched) if fetched else None,
                        ai_score=a.get("ai_score"),
                        ai_score_reason=a.get("ai_score_reason"),
                        ai_summary=a.get("ai_summary"),
                        first_principle=a.get("first_principle"),
                        key_insight=a.get("key_insight"),
                        ai_insight=a.get("ai_insight"),
                        ai_article_analysis=a.get("ai_article_analysis"),
                    ))
                upserted += 1
            except Exception as exc:
                logger.warning("sync_from_json: failed on %s: %s", url, exc)
                db.rollback()
                continue
        try:
            db.commit()
        except Exception as exc:
            logger.warning("sync_from_json: commit failed: %s", exc)
            db.rollback()
        logger.info("sync_from_json: upserted %d articles", upserted)
        return upserted

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
                        title=_clean_title(entry.get("title", "Untitled"))[:500],
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

    def get_article(self, db: Session, article_id: int) -> Optional[FeedArticle]:
        return db.query(FeedArticle).filter(FeedArticle.id == article_id).first()

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
