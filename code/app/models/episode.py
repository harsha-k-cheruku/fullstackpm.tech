from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Episode(Base):
    __tablename__ = "podcast_episodes"

    id = Column(String, primary_key=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    episode_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    published_at = Column(DateTime, nullable=False)
    duration_seconds = Column(Integer)
    duration_human = Column(String)
    audio_url = Column(String, nullable=False)
    shownotes_html = Column(Text)
    curriculum_lesson = Column(String)
    spy_close = Column(Float)
    spy_pct_change = Column(Float)
    iv_rank = Column(Float)
    tags = Column(String)
    status = Column(String, default="complete")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
