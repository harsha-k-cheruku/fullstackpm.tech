# app/models/like.py
"""Like model for blog posts."""
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class Like(Base):
    """One like per user_id per blog post slug."""

    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("blog_post_slug", "user_id", name="uq_like_per_user"),)

    id = Column(Integer, primary_key=True, index=True)
    blog_post_slug = Column(String, index=True, nullable=False)
    user_id = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
