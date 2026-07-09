"""Stage 3: Claude reads full article text → structured analysis + score.

ONE Claude call per article produces: display_title, score, score_reason,
takeaways, pull_quote, pm_implication, contrarian, prose_analysis.

Append-only: each run inserts a new article_analyses row and flips is_latest.
Also denormalizes the latest values into feed_articles so existing Render
templates keep working unchanged.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import Optional

from pipeline import config

from app.database import SessionLocal, ensure_feed_layer2_columns, ensure_pipeline_tables, init_db
from app.models.feed_article import FeedArticle
from app.models.pipeline_models import ArticleAnalysis, ArticleExtract


SYSTEM_PROMPT = """You are a senior PM analyst reading a full article for a busy product manager. Extract everything substantive in structured form.

Return JSON with exactly these keys:

{
  "display_title": "5-9 word newspaper headline. Specific noun + action. NO episode numbers, NO 'Weekly X #N', NO vague phrases like 'Some thoughts on'. Example: 'DuckDB Adds Persistent Storage In 1.0 Release' not 'Weekly Dose of Optimism #195'.",
  "score": <integer 1-10>,
  "score_reason": "one sentence on why this score",
  "takeaways": [
    "5-7 strings. Each one a SPECIFIC concrete insight from THIS article (not generic advice). What does THIS article actually say?"
  ],
  "pull_quote": "The single sentence from the article that crystallizes its argument. Verbatim if possible, close paraphrase if needed for clarity.",
  "pm_implication": "One sentence: what should a PM do or think differently after reading this?",
  "contrarian": "The catch, risk, or counter-argument the author understates or misses. Be sharp.",
  "prose_analysis": "200 words of YOUR analysis (a smart peer briefing another PM). Not a summary — your read on what matters, what's missed, what to watch for. Specific, direct, no filler."
}

Scoring scale:
  8-10: directly actionable or strategically important for a senior B2B SaaS PM
  5-7: interesting context, not urgent
  1-4: too niche, generic, sponsored, hiring posts, or low-effort content

Rules:
- All output is YOUR voice (smart peer briefing another PM), not the article's voice
- Takeaways must be SPECIFIC to what THIS article says, not category platitudes
- No markdown, no bullet symbols, no headers
- Return ONLY valid JSON. No code fences. No prose around it."""


def _build_user_prompt(article: FeedArticle, full_text: str) -> str:
    return (
        f"Source: {article.source_name}\n"
        f"Category: {article.source_category}\n"
        f"Original title: {article.title}\n"
        f"URL: {article.url}\n\n"
        f"FULL ARTICLE TEXT:\n{full_text[:12000]}\n\n"
        "Return the JSON object now."
    )


def _call_claude(prompt: str) -> Optional[str]:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=config.ANALYSE_MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as exc:
        print(f"  ! Claude call failed: {exc}")
        return None


def _parse_json(raw: str) -> Optional[dict]:
    cleaned = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence:
        cleaned = fence.group(1).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        print(f"  ! JSON parse failed: {exc}\n    raw: {raw[:200]}...")
        return None


def _denormalize_to_feed_article(article: FeedArticle, analysis: "ArticleAnalysis"):
    """Mirror latest analysis values onto feed_articles so existing Render
    templates (which read FeedArticle columns) keep working."""
    article.display_title = analysis.display_title
    article.ai_score = analysis.score
    article.ai_score_reason = analysis.score_reason
    article.ai_article_analysis = analysis.prose_analysis
    article.ai_processed_at = analysis.run_at

    # Map category-specific insight field
    insight = analysis.pm_implication or ""
    cat = (article.source_category or "").lower()
    if cat == "engineering":
        article.ai_summary = insight
    elif cat == "strategy":
        article.first_principle = insight
    elif cat == "pm":
        article.key_insight = insight
    elif cat == "ai":
        article.ai_insight = insight


def run(limit: Optional[int] = None, re_analyse: bool = False) -> dict:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {"stage": "analyse", "error": "ANTHROPIC_API_KEY not set"}

    init_db()
    ensure_feed_layer2_columns()
    ensure_pipeline_tables()

    db = SessionLocal()
    try:
        # Find articles with a successful extract that haven't been analysed (latest run)
        # If re_analyse, include all with extracts.
        all_extracted_ids = {
            row.article_id for row in
            db.query(ArticleExtract.article_id).filter(ArticleExtract.success == True).all()
        }

        if not re_analyse:
            already_analysed_ids = {
                row.article_id for row in
                db.query(ArticleAnalysis.article_id).filter(ArticleAnalysis.is_latest == True).all()
            }
            target_ids = all_extracted_ids - already_analysed_ids
        else:
            target_ids = all_extracted_ids

        articles = (
            db.query(FeedArticle)
            .filter(FeedArticle.id.in_(target_ids))
            .filter(FeedArticle.is_dismissed == False)
            .order_by(FeedArticle.fetched_at.desc())
            .all()
        )

        cap = limit or config.MAX_ANALYSE_PER_RUN
        articles = articles[:cap]

        ok = failed = 0
        for article in articles:
            extract = (
                db.query(ArticleExtract)
                .filter(ArticleExtract.article_id == article.id)
                .filter(ArticleExtract.success == True)
                .order_by(ArticleExtract.fetched_at.desc())
                .first()
            )
            if not extract or not extract.full_text:
                failed += 1
                continue

            raw = _call_claude(_build_user_prompt(article, extract.full_text))
            if not raw:
                failed += 1
                continue

            data = _parse_json(raw)
            if not data:
                failed += 1
                continue

            # Demote prior latest for this article
            db.query(ArticleAnalysis).filter(
                ArticleAnalysis.article_id == article.id,
                ArticleAnalysis.is_latest == True,
            ).update({"is_latest": False})

            score = data.get("score")
            try:
                score = max(1, min(int(score), 10)) if score is not None else None
            except (ValueError, TypeError):
                score = None

            analysis = ArticleAnalysis(
                article_id=article.id,
                run_at=datetime.utcnow(),
                model=config.ANALYSE_MODEL,
                prompt_version=config.ANALYSE_PROMPT_VERSION,
                is_latest=True,
                display_title=(data.get("display_title") or "")[:300] or None,
                score=score,
                score_reason=(data.get("score_reason") or "")[:1000] or None,
                takeaways_json=json.dumps(data.get("takeaways") or []),
                pull_quote=data.get("pull_quote"),
                pm_implication=data.get("pm_implication"),
                contrarian=data.get("contrarian"),
                prose_analysis=data.get("prose_analysis"),
            )
            db.add(analysis)
            db.flush()

            _denormalize_to_feed_article(article, analysis)
            db.commit()
            ok += 1
            print(f"  ✓ [{article.id}] score={analysis.score} — {analysis.display_title}")

        return {"stage": "analyse", "attempted": len(articles), "success": ok, "failed": failed}
    finally:
        db.close()


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
