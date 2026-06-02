# app/models/pipeline_models.py
"""Append-only history tables for the editorial pipeline.

Raw → analyses → editorials. Each analyse/rewrite run inserts a new row.
`is_latest` flag marks the current "winning" version. Render reads the latest.

deep_dives table is stubbed for the backlog AI-vs-AI conversation feature.
"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from app.database import Base


class ArticleExtract(Base):
    """Cached full-text scrape of a source article."""
    __tablename__ = "article_extracts"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("feed_articles.id"), nullable=False, index=True)
    full_text = Column(Text, nullable=True)
    char_count = Column(Integer, nullable=True)
    extractor = Column(String(50), nullable=True)   # "trafilatura", "readability", etc.
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    success = Column(Boolean, default=False, nullable=False)
    error = Column(Text, nullable=True)


class ArticleAnalysis(Base):
    """One AI analysis run. Append-only — re-runs insert new rows."""
    __tablename__ = "article_analyses"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("feed_articles.id"), nullable=False, index=True)
    run_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model = Column(String(100), nullable=False)
    prompt_version = Column(String(50), nullable=False)
    is_latest = Column(Boolean, default=True, nullable=False, index=True)

    # Analysis outputs
    display_title = Column(String(300), nullable=True)
    score = Column(Integer, nullable=True)
    score_reason = Column(Text, nullable=True)
    takeaways_json = Column(Text, nullable=True)        # JSON list of strings
    pull_quote = Column(Text, nullable=True)
    pm_implication = Column(Text, nullable=True)
    contrarian = Column(Text, nullable=True)
    prose_analysis = Column(Text, nullable=True)


class ArticleEditorial(Base):
    """A rewrite — polished editorial version in HC's voice. Append-only, drafts allowed."""
    __tablename__ = "article_editorials"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("feed_articles.id"), nullable=False, index=True)
    analysis_id = Column(Integer, ForeignKey("article_analyses.id"), nullable=True)
    run_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model = Column(String(100), nullable=False)
    prompt_version = Column(String(50), nullable=False)
    status = Column(String(20), default="draft", nullable=False)  # draft | published | archived
    is_published = Column(Boolean, default=False, nullable=False, index=True)

    headline = Column(String(300), nullable=True)
    dek = Column(String(500), nullable=True)            # one-line subhead
    lede = Column(Text, nullable=True)                  # opening paragraph
    body = Column(Text, nullable=True)                  # full piece (400-600 words)


class DeepDive(Base):
    """Backlog: multi-AI conversation episode. Schema only — no logic yet."""
    __tablename__ = "deep_dives"

    id = Column(Integer, primary_key=True)
    source_article_id = Column(Integer, ForeignKey("feed_articles.id"), nullable=True)
    topic = Column(String(500), nullable=True)
    format = Column(String(50), nullable=True)          # "unpack" | "commentary"
    participants_json = Column(Text, nullable=True)     # [{model, persona, voice}, ...]
    transcript_json = Column(Text, nullable=True)       # [{speaker, text}, ...]
    audio_url = Column(String(1000), nullable=True)
    status = Column(String(20), default="draft", nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
