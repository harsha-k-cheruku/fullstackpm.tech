# app/models/feed_article.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class FeedArticle(Base):
    __tablename__ = "feed_articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    excerpt = Column(Text, nullable=True)
    source_name = Column(String(200), nullable=False)
    source_category = Column(String(50), nullable=False)
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    is_editors_pick = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)

    # Layer 2: AI enrichment
    ai_summary = Column(Text, nullable=True)        # engineering: PM-lens explanation
    first_principle = Column(Text, nullable=True)   # strategy: mental model extraction
    key_insight = Column(Text, nullable=True)       # pm: actionable takeaway
    ai_insight = Column(Text, nullable=True)        # ai: so what for PMs
    ai_score = Column(Integer, nullable=True)       # 1-10 PM relevance score
    ai_score_reason = Column(Text, nullable=True)   # one sentence explaining score
    ai_processed_at = Column(DateTime, nullable=True)
    ai_article_analysis = Column(Text, nullable=True)
    display_title = Column(String(300), nullable=True)  # cleaned headline, falls back to title
