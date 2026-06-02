"""Stage 4: rewrite — top N analysed articles get a polished editorial in HC's voice.

Reads the latest ArticleAnalysis per article. Produces an ArticleEditorial draft
(status='draft'). HC reviews and flips status='published' via the editorial UI.
"""
import json
import os
import re
from datetime import datetime

from pipeline import config

from app.database import SessionLocal, ensure_pipeline_tables, init_db
from app.models.feed_article import FeedArticle
from app.models.pipeline_models import ArticleAnalysis, ArticleEditorial


SYSTEM_PROMPT = """You are Harsha Cheruku, a senior product manager who writes fullstackpm.tech. You've just read an article and your analyst's structured notes on it. Now write a polished editorial piece in YOUR voice.

Your voice: direct, contrarian-when-warranted, useful. You write for working PMs who want to skip hot takes and get to what actually matters. You name trade-offs others gloss over. You connect specific stories to durable principles. You don't hedge, but you also don't oversell. When the source is wrong or misleading, you say so.

Return JSON with exactly these keys:

{
  "headline": "YOUR headline — different from the source. Specific, with a point of view. 6-10 words.",
  "dek": "One-line subhead beneath the headline. Sets up the tension or insight. Under 120 chars.",
  "lede": "Opening paragraph (2-3 sentences) that hooks. Start with the most surprising or important thing. No 'in this article' or 'recently'.",
  "body": "The full piece, 400-600 words. Structure: context (what happened, briefly) → analysis (what it means, why it matters) → so-what for PMs (what to do or watch). Crisp prose. Specific examples. End with a sharp observation, not a summary."
}

Rules:
- This is YOUR voice — opinionated, specific, useful
- You don't have to agree with the source — push back where warranted
- Use the analyst notes (takeaways, contrarian, pm_implication) as raw material, not a script
- No markdown, no bullet symbols, no headers in the body
- Return ONLY valid JSON. No code fences. No prose around it."""


def _build_user_prompt(article: FeedArticle, analysis: ArticleAnalysis) -> str:
    takeaways = []
    if analysis.takeaways_json:
        try:
            takeaways = json.loads(analysis.takeaways_json)
        except json.JSONDecodeError:
            pass
    bullets = "\n".join(f"- {t}" for t in takeaways) if takeaways else "(none)"

    return f"""SOURCE: {article.source_name}
CATEGORY: {article.source_category}
ORIGINAL TITLE: {article.title}
URL: {article.url}

ANALYST'S DISPLAY TITLE: {analysis.display_title}

KEY TAKEAWAYS:
{bullets}

PULL QUOTE FROM ARTICLE:
{analysis.pull_quote or '(none)'}

ANALYST'S PROSE ANALYSIS:
{analysis.prose_analysis or '(none)'}

PM IMPLICATION:
{analysis.pm_implication or '(none)'}

CONTRARIAN READ:
{analysis.contrarian or '(none)'}

Now write the editorial piece. Return the JSON object."""


def _call_claude(prompt: str) -> str | None:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=config.REWRITE_MODEL,
            max_tokens=2500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as exc:
        print(f"  ! Claude call failed: {exc}")
        return None


def _parse_json(raw: str) -> dict | None:
    cleaned = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence:
        cleaned = fence.group(1).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        print(f"  ! JSON parse failed: {exc}\n    raw: {raw[:200]}...")
        return None


def run(top_n: int | None = None, re_rewrite: bool = False) -> dict:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {"stage": "rewrite", "error": "ANTHROPIC_API_KEY not set"}

    init_db()
    ensure_pipeline_tables()

    n = top_n or config.REWRITE_TOP_N

    db = SessionLocal()
    try:
        # Find candidates: latest analyses with score >= floor, sorted by score desc
        candidates = (
            db.query(ArticleAnalysis, FeedArticle)
            .join(FeedArticle, FeedArticle.id == ArticleAnalysis.article_id)
            .filter(ArticleAnalysis.is_latest == True)
            .filter(ArticleAnalysis.score >= config.MIN_PUBLISH_SCORE)
            .filter(FeedArticle.is_dismissed == False)
            .order_by(ArticleAnalysis.score.desc())
            .limit(n * 3)  # over-fetch — we'll filter already-rewritten
            .all()
        )

        if not re_rewrite:
            already_done_ids = {
                row.article_id for row in
                db.query(ArticleEditorial.article_id).all()
            }
            candidates = [(a, art) for a, art in candidates if art.id not in already_done_ids]

        candidates = candidates[:n]

        ok = failed = 0
        for analysis, article in candidates:
            raw = _call_claude(_build_user_prompt(article, analysis))
            if not raw:
                failed += 1
                continue
            data = _parse_json(raw)
            if not data:
                failed += 1
                continue

            editorial = ArticleEditorial(
                article_id=article.id,
                analysis_id=analysis.id,
                run_at=datetime.utcnow(),
                model=config.REWRITE_MODEL,
                prompt_version=config.REWRITE_PROMPT_VERSION,
                status="draft",
                is_published=False,
                headline=(data.get("headline") or "")[:300] or None,
                dek=(data.get("dek") or "")[:500] or None,
                lede=data.get("lede"),
                body=data.get("body"),
            )
            db.add(editorial)
            db.commit()
            ok += 1
            print(f"  ✓ [{article.id}] {editorial.headline}")

        return {"stage": "rewrite", "candidates": len(candidates), "drafted": ok, "failed": failed}
    finally:
        db.close()


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
