#!/usr/bin/env python3
"""
Local feed processing script — run on your machine, not on Render.

Does the heavy work: fetch RSS → score articles → generate analyses → sync to Render.
Render only serves; all AI calls happen here.

Setup (once):
  cd /Users/sidc/Projects/claude_code/fullstackpm.tech/code
  source venv/bin/activate
  export ANTHROPIC_API_KEY=sk-ant-...
  export EDITORIAL_TOKEN=fspm-editorial-2026

Run:
  python scripts/process_feed.py               # full pipeline + sync
  python scripts/process_feed.py --no-sync     # process locally only, don't push to Render
  python scripts/process_feed.py --sync-only   # skip processing, just push existing local DB to Render
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

# Make app importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))

# Use a local DB separate from Render's
os.environ.setdefault("DATABASE_URL", "sqlite:///./local_feed.db")

from app.database import SessionLocal, init_db, ensure_feed_layer2_columns
from app.models.feed_article import FeedArticle
from app.services.feed_service import feed_service
from app.services.ai_processing_service import ai_processing_service

RENDER_URL = os.environ.get("RENDER_URL", "https://fullstackpm.tech")
EDITORIAL_TOKEN = os.environ.get("EDITORIAL_TOKEN", "fspm-editorial-2026")
MAX_ANALYSIS_PER_RUN = 50  # cap to avoid very long runs; increase as needed


def setup_db():
    init_db()
    ensure_feed_layer2_columns()


def fetch_and_score(db):
    new = feed_service.fetch_all(db)
    print(f"  RSS fetch: {new} new articles")

    scored = ai_processing_service.process_unprocessed(db, limit=200)
    print(f"  AI scoring: {scored} articles scored")
    return new, scored


def generate_analyses(db):
    pending = (
        db.query(FeedArticle)
        .filter(FeedArticle.ai_processed_at.isnot(None))
        .filter(FeedArticle.ai_article_analysis.is_(None))
        .filter(FeedArticle.is_dismissed == False)
        .order_by(FeedArticle.ai_score.desc().nullslast())
        .limit(MAX_ANALYSIS_PER_RUN)
        .all()
    )
    print(f"  Generating analyses for {len(pending)} articles (cap {MAX_ANALYSIS_PER_RUN}/run)...")
    done = 0
    for article in pending:
        result = ai_processing_service.generate_article_analysis(article, db)
        if result:
            done += 1
    print(f"  Analyses generated: {done}")
    return done


def serialize(a: FeedArticle) -> dict:
    return {
        "url": a.url,
        "title": a.title,
        "display_title": a.display_title,
        "excerpt": a.excerpt,
        "source_name": a.source_name,
        "source_category": a.source_category,
        "published_at": a.published_at.isoformat() if a.published_at else None,
        "ai_score": a.ai_score,
        "ai_score_reason": a.ai_score_reason,
        "ai_summary": a.ai_summary,
        "first_principle": a.first_principle,
        "key_insight": a.key_insight,
        "ai_insight": a.ai_insight,
        "ai_article_analysis": a.ai_article_analysis,
        "ai_processed_at": a.ai_processed_at.isoformat() if a.ai_processed_at else None,
    }


def sync_to_render(db):
    articles = (
        db.query(FeedArticle)
        .filter(FeedArticle.is_dismissed == False)
        .all()
    )
    payload = json.dumps({"articles": [serialize(a) for a in articles]}).encode()
    url = f"{RENDER_URL}/api/feed/sync?token={urllib.parse.quote(EDITORIAL_TOKEN)}"
    print(f"  Syncing {len(articles)} articles to {RENDER_URL}...")
    try:
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        print(f"  Sync complete: {result}")
    except Exception as exc:
        print(f"  Sync failed: {exc}")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-sync", action="store_true", help="Skip pushing to Render")
    parser.add_argument("--sync-only", action="store_true", help="Skip processing, just sync")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY") and not args.sync_only:
        print("ERROR: ANTHROPIC_API_KEY not set. Export it first:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    print("=== process_feed.py ===")
    setup_db()
    db = SessionLocal()
    try:
        if not args.sync_only:
            print("\n[1/3] Fetch + Score")
            fetch_and_score(db)

            print("\n[2/3] Generate Analyses")
            generate_analyses(db)
        else:
            print("\n[skip] Processing skipped (--sync-only)")

        if not args.no_sync:
            print("\n[3/3] Sync to Render")
            sync_to_render(db)
        else:
            print("\n[skip] Sync skipped (--no-sync)")

        print("\nDone.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
