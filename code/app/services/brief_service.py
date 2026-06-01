# app/services/brief_service.py
from __future__ import annotations

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.models.feed_article import FeedArticle

logger = logging.getLogger(__name__)

BRIEF_VOICE = "en-US-AriaNeural"
MAX_STORY_COUNT = 6
MIN_STORY_COUNT = 3

_SCRIPT_SYSTEM = """You are the host of "PM Daily Brief" — a crisp, intelligent 5-minute audio show for senior product managers.

Write a podcast script from the provided top stories. Rules:
- Under 500 words total
- Plain text only — no markdown, no headers, no bullet points
- Conversational but confident — no filler words ("um", "so", "basically", "you know", "kind of")
- Present insights peer-to-peer, not teacher-to-student
- Each story: say the source name, the title or topic, then the key insight naturally woven in, then a brief transition
- Intro: "Good [morning/afternoon]. Here's your PM Intelligence Brief for {date}."
- Outro: "That's your PM brief for today. Full coverage at fullstackpm.tech. Stay sharp."
- Do not add section labels or numbering — just the spoken words"""


def _build_script_prompt(articles: list[FeedArticle], brief_date: str) -> str:
    stories = []
    for article in articles:
        insight = (
            article.ai_summary
            or article.first_principle
            or article.key_insight
            or article.ai_insight
            or article.excerpt
            or ""
        )
        stories.append(
            {
                "source": article.source_name,
                "category": article.source_category,
                "title": article.title,
                "score": article.ai_score,
                "insight": insight[:300],
            }
        )
    return (
        f"Date: {brief_date}\n\n"
        f"Top stories ({len(stories)}):\n"
        + json.dumps(stories, indent=2)
        + "\n\nWrite the podcast script now."
    )


def _get_audio_dir() -> Path:
    audio_dir = settings.static_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    return audio_dir


def _get_manifest_path() -> Path:
    return _get_audio_dir() / "pm-brief-manifest.json"


def _load_manifest() -> dict:
    path = _get_manifest_path()
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return {"episodes": []}


def _save_manifest(manifest: dict) -> None:
    _get_manifest_path().write_text(json.dumps(manifest, indent=2, default=str))


def _today_brief_exists() -> bool:
    today = date.today().isoformat()
    manifest = _load_manifest()
    return any(ep.get("date") == today for ep in manifest.get("episodes", []))


class BriefService:
    async def generate_if_needed(self, db: Session) -> bool:
        """Generate today's brief if it doesn't exist yet. Returns True if generated."""
        if _today_brief_exists():
            logger.info("Today's PM brief already exists — skipping")
            return False
        return await self.generate(db)

    async def generate(self, db: Session) -> bool:
        """Generate a fresh brief for today. Returns True on success."""
        articles = self._get_brief_articles(db)
        if len(articles) < MIN_STORY_COUNT:
            logger.warning("Not enough scored articles for brief (got %d, need %d)", len(articles), MIN_STORY_COUNT)
            return False

        today = date.today()
        brief_date = today.strftime("%B %d, %Y")
        date_slug = today.isoformat()
        audio_filename = f"pm-brief-{date_slug}.mp3"
        audio_path = _get_audio_dir() / audio_filename

        script = self._generate_script(articles, brief_date)
        if not script:
            logger.error("Script generation failed — skipping audio")
            return False

        success = await self._generate_audio(script, audio_path)
        if not success:
            return False

        self._update_manifest(
            date_slug=date_slug,
            title=f"PM Daily Brief — {brief_date}",
            audio_filename=audio_filename,
            article_count=len(articles),
            script=script,
        )
        logger.info("PM brief generated: %s (%d stories)", audio_filename, len(articles))
        return True

    def _get_brief_articles(self, db: Session) -> list[FeedArticle]:
        picks = (
            db.query(FeedArticle)
            .filter(
                FeedArticle.is_editors_pick == True,
                FeedArticle.is_dismissed == False,
                FeedArticle.ai_score.isnot(None),
            )
            .order_by(FeedArticle.ai_score.desc())
            .limit(MAX_STORY_COUNT)
            .all()
        )
        if len(picks) >= MIN_STORY_COUNT:
            return picks

        return (
            db.query(FeedArticle)
            .filter(
                FeedArticle.is_dismissed == False,
                FeedArticle.ai_score >= 7,
            )
            .order_by(FeedArticle.ai_score.desc(), FeedArticle.fetched_at.desc())
            .limit(MAX_STORY_COUNT)
            .all()
        )

    def _generate_script(self, articles: list[FeedArticle], brief_date: str) -> Optional[str]:
        if not settings.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY not set — using excerpt-only script")
            return self._fallback_script(articles, brief_date)
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=settings.anthropic_api_key)
            response = client.messages.create(
                model=settings.anthropic_model,
                max_tokens=700,
                system=_SCRIPT_SYSTEM,
                messages=[{"role": "user", "content": _build_script_prompt(articles, brief_date)}],
            )
            return response.content[0].text.strip()
        except Exception as exc:
            logger.error("Script generation failed: %s", exc)
            return self._fallback_script(articles, brief_date)

    def _fallback_script(self, articles: list[FeedArticle], brief_date: str) -> str:
        lines = [f"Good morning. Here's your PM Intelligence Brief for {brief_date}."]
        for article in articles:
            insight = (
                article.ai_summary
                or article.first_principle
                or article.key_insight
                or article.ai_insight
                or article.excerpt
                or ""
            )
            lines.append(f"From {article.source_name}: {article.title}. {insight}")
        lines.append("That's your PM brief for today. Full coverage at fullstackpm.tech. Stay sharp.")
        return " ".join(lines)

    async def _generate_audio(self, script: str, output_path: Path) -> bool:
        try:
            import edge_tts

            communicate = edge_tts.Communicate(script, BRIEF_VOICE)
            await communicate.save(str(output_path))
            return True
        except Exception as exc:
            logger.error("Edge TTS audio generation failed: %s", exc)
            return False

    def _update_manifest(
        self,
        date_slug: str,
        title: str,
        audio_filename: str,
        article_count: int,
        script: str,
    ) -> None:
        manifest = _load_manifest()
        audio_url = f"{settings.site_url}/static/audio/{audio_filename}"
        episode = {
            "date": date_slug,
            "title": title,
            "audio_url": audio_url,
            "audio_filename": audio_filename,
            "article_count": article_count,
            "script": script,
            "generated_at": datetime.utcnow().isoformat(),
        }
        episodes = [ep for ep in manifest.get("episodes", []) if ep.get("date") != date_slug]
        episodes.insert(0, episode)
        manifest["episodes"] = episodes[:30]
        _save_manifest(manifest)

    def get_latest(self) -> Optional[dict]:
        """Return the most recent episode from the manifest."""
        manifest = _load_manifest()
        episodes = manifest.get("episodes", [])
        return episodes[0] if episodes else None

    def get_all(self) -> list[dict]:
        """Return all episodes from the manifest."""
        return _load_manifest().get("episodes", [])


brief_service = BriefService()
