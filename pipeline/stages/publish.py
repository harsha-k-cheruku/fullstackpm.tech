"""Stage 5: publish — DB → JSON files committed to git.

Writes:
  code/content/feed/articles.json         — feed listing (lightweight)
  code/content/feed/articles/{slug}.json  — full per-article data
  code/content/feed/manifest.json         — published_at + counts

Render reads these JSON files at boot (loader to be added in next phase).
Until that loader exists, this stage still produces JSON locally so you can
inspect what would be published.
"""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from typing import Dict, Optional

from pipeline import config

from app.database import SessionLocal, ensure_pipeline_tables, init_db
from app.models.feed_article import FeedArticle
from app.models.pipeline_models import ArticleAnalysis, ArticleEditorial


def _slugify(text: str, fallback_id: int) -> str:
    if not text:
        return f"article-{fallback_id}"
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", norm).strip("-").lower()
    slug = slug[:80] or f"article-{fallback_id}"
    return f"{slug}-{fallback_id}"


def _serialize_article(article: FeedArticle, analysis: Optional[ArticleAnalysis], editorial: Optional[ArticleEditorial]) -> dict:
    takeaways = []
    if analysis and analysis.takeaways_json:
        try:
            takeaways = json.loads(analysis.takeaways_json)
        except json.JSONDecodeError:
            pass

    slug = _slugify(
        (editorial.headline if editorial else None) or
        (analysis.display_title if analysis else None) or
        article.title,
        article.id,
    )

    return {
        "id": article.id,
        "slug": slug,
        "url": article.url,
        "title": article.title,
        "source_name": article.source_name,
        "source_category": article.source_category,
        "published_at": article.published_at.isoformat() if article.published_at else None,
        "fetched_at": article.fetched_at.isoformat() if article.fetched_at else None,
        "is_editors_pick": bool(article.is_editors_pick),
        "analysis": {
            "display_title": analysis.display_title if analysis else None,
            "score": analysis.score if analysis else None,
            "score_reason": analysis.score_reason if analysis else None,
            "takeaways": takeaways,
            "pull_quote": analysis.pull_quote if analysis else None,
            "pm_implication": analysis.pm_implication if analysis else None,
            "contrarian": analysis.contrarian if analysis else None,
            "prose_analysis": analysis.prose_analysis if analysis else None,
            "run_at": analysis.run_at.isoformat() if analysis else None,
        } if analysis else None,
        "editorial": {
            "headline": editorial.headline,
            "dek": editorial.dek,
            "lede": editorial.lede,
            "body": editorial.body,
            "published_at": editorial.run_at.isoformat(),
        } if editorial else None,
    }


def run(include_drafts: bool = False) -> dict:
    init_db()
    ensure_pipeline_tables()

    db = SessionLocal()
    try:
        # Latest analysis per article
        analyses_by_id = {
            a.article_id: a for a in
            db.query(ArticleAnalysis).filter(ArticleAnalysis.is_latest == True).all()
        }

        # Latest editorial per article (prefer published, else most recent draft)
        all_editorials = (
            db.query(ArticleEditorial)
            .order_by(ArticleEditorial.is_published.desc(), ArticleEditorial.run_at.desc())
            .all()
        )
        editorial_by_id: Dict[int, ArticleEditorial] = {}
        for ed in all_editorials:
            if ed.article_id not in editorial_by_id:
                if include_drafts or ed.is_published:
                    editorial_by_id[ed.article_id] = ed

        # Eligible articles: not dismissed, has analysis, score >= floor
        articles = (
            db.query(FeedArticle)
            .filter(FeedArticle.is_dismissed == False)
            .all()
        )

        published_articles = []
        for article in articles:
            analysis = analyses_by_id.get(article.id)
            if not analysis or (analysis.score or 0) < config.MIN_PUBLISH_SCORE:
                continue
            editorial = editorial_by_id.get(article.id)
            published_articles.append(_serialize_article(article, analysis, editorial))

        # Sort: editor's pick first, then by score, then recency
        published_articles.sort(key=lambda a: (
            -1 if a["is_editors_pick"] else 0,
            -(a["analysis"]["score"] or 0),
            -(a["analysis"]["run_at"] or ""),
        ))

        # Write per-article JSONs
        articles_dir = config.PUBLISH_DIR / "articles"
        articles_dir.mkdir(parents=True, exist_ok=True)
        for entry in published_articles:
            path = articles_dir / f"{entry['slug']}.json"
            path.write_text(json.dumps(entry, indent=2))

        # Write feed listing (light version — no full body/analysis)
        listing = [{
            "id": a["id"],
            "slug": a["slug"],
            "url": a["url"],
            "source_name": a["source_name"],
            "source_category": a["source_category"],
            "is_editors_pick": a["is_editors_pick"],
            "headline": (a["editorial"]["headline"] if a["editorial"] else None) or (a["analysis"]["display_title"] if a["analysis"] else a["title"]),
            "dek": a["editorial"]["dek"] if a["editorial"] else None,
            "pm_implication": a["analysis"]["pm_implication"] if a["analysis"] else None,
            "score": a["analysis"]["score"] if a["analysis"] else None,
            "published_at": a["published_at"],
        } for a in published_articles]

        feed_path = config.PUBLISH_DIR / "articles.json"
        feed_path.write_text(json.dumps(listing, indent=2))

        manifest = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_published": len(published_articles),
            "by_category": {},
        }
        for a in published_articles:
            cat = a["source_category"] or "unknown"
            manifest["by_category"][cat] = manifest["by_category"].get(cat, 0) + 1
        (config.PUBLISH_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

        print(f"  Wrote {len(published_articles)} articles to {config.PUBLISH_DIR}")
        return {"stage": "publish", "published": len(published_articles), "path": str(config.PUBLISH_DIR)}
    finally:
        db.close()


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
