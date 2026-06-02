"""Stage 2: fetch each article URL, extract clean body text via trafilatura.

No AI. Cached per-article in article_extracts (one row per attempt, latest wins
in practice — we query with order_by fetched_at desc).
"""
from datetime import datetime

from pipeline import config

from app.database import SessionLocal, ensure_pipeline_tables, init_db
from app.models.feed_article import FeedArticle
from app.models.pipeline_models import ArticleExtract


def _extract(url: str) -> tuple[str | None, str | None]:
    """Return (full_text, error). One of them is None."""
    try:
        import trafilatura
    except ImportError:
        return None, "trafilatura not installed — pip install -r pipeline/requirements.txt"

    try:
        downloaded = trafilatura.fetch_url(url, timeout=config.EXTRACT_TIMEOUT_SECONDS)
        if not downloaded:
            return None, "fetch returned empty"
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
            favor_recall=True,
        )
        if not text or len(text.strip()) < 200:
            return None, f"extracted text too short ({len(text or '')} chars)"
        return text.strip(), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def run(limit: int | None = None, re_extract: bool = False) -> dict:
    init_db()
    ensure_pipeline_tables()

    db = SessionLocal()
    try:
        # Find articles that need extraction
        query = db.query(FeedArticle).filter(FeedArticle.is_dismissed == False)
        if not re_extract:
            already_extracted_ids = {
                row.article_id for row in
                db.query(ArticleExtract.article_id).filter(ArticleExtract.success == True).all()
            }
            articles = [a for a in query.all() if a.id not in already_extracted_ids]
        else:
            articles = query.all()

        if limit:
            articles = articles[:limit]

        ok = failed = 0
        for article in articles:
            text, error = _extract(article.url)
            extract = ArticleExtract(
                article_id=article.id,
                full_text=text,
                char_count=len(text) if text else 0,
                extractor="trafilatura",
                fetched_at=datetime.utcnow(),
                success=bool(text),
                error=error,
            )
            db.add(extract)
            db.commit()
            if text:
                ok += 1
                print(f"  ✓ [{article.id}] {len(text)} chars — {article.title[:60]}")
            else:
                failed += 1
                print(f"  ✗ [{article.id}] {error} — {article.title[:60]}")

        return {"stage": "extract", "attempted": len(articles), "success": ok, "failed": failed}
    finally:
        db.close()


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
