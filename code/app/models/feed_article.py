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
