from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class NaradaOverride(Base):
    """Per-pipeline editorial overrides set via the admin UI.

    One row per pipeline (morning / afternoon). The Mac mini pipeline GETs
    /api/narada/config before each run and merges these overrides with its
    local config.yaml and notes.md.
    """

    __tablename__ = "narada_overrides"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline = Column(String, default="morning", unique=True, nullable=False)

    # Segment toggles
    global_news_enabled = Column(Boolean, default=True, nullable=False)
    spy_learning_enabled = Column(Boolean, default=True, nullable=False)
    market_brief_enabled = Column(Boolean, default=True, nullable=False)
    analytics_pm_enabled = Column(Boolean, default=True, nullable=False)

    # Editorial notes — fed into the distiller as guidance
    notes_general = Column(Text, default="")
    notes_news = Column(Text, default="")
    notes_spy = Column(Text, default="")
    notes_market = Column(Text, default="")
    notes_pm = Column(Text, default="")

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)
