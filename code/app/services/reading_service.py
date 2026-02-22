# app/services/reading_service.py
from __future__ import annotations

import json
import time
from pathlib import Path

import feedparser

# Pre-approved RSS feeds — edit this list to change auto-pulled content
RSS_FEEDS = [
    {
        "name": "Lenny's Newsletter",
        "url": "https://www.lennysnewsletter.com/feed",
        "type": "essay",
        "max_items": 2,
    },
    {
        "name": "Product Talk",
        "url": "https://www.producttalk.org/feed/",
        "type": "essay",
        "max_items": 1,
    },
]

_CACHE_TTL = 3600  # 1 hour


class ReadingService:
    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path
        self._rss_cache: list[dict] = []
        self._cache_time: float = 0.0

    def _load_manual_picks(self) -> list[dict]:
        try:
            path = self._data_path / "reading_stack.json"
            with open(path) as f:
                data = json.load(f)
            return data.get("picks", []), data.get("last_updated", "")
        except Exception:
            return [], ""

    def _fetch_rss(self) -> list[dict]:
        now = time.time()
        if self._rss_cache and (now - self._cache_time) < _CACHE_TTL:
            return self._rss_cache

        items: list[dict] = []
        for feed_config in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_config["url"])
                for entry in feed.entries[: feed_config["max_items"]]:
                    items.append(
                        {
                            "type": feed_config["type"],
                            "title": entry.get("title", "Untitled"),
                            "source": feed_config["name"],
                            "url": entry.get("link", "#"),
                            "note": None,
                            "auto": True,
                        }
                    )
            except Exception:
                # Silently skip — a broken feed shouldn't crash the homepage
                pass

        self._rss_cache = items
        self._cache_time = now
        return items

    def get(self) -> dict:
        picks, last_updated = self._load_manual_picks()
        rss = self._fetch_rss()
        return {
            "picks": picks,
            "rss": rss,
            "last_updated": last_updated,
        }
