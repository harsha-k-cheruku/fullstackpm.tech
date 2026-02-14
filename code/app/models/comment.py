# app/models/comment.py
"""Comment model for blog posts."""
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func

from app.database import Base


class Comment(Base):
    """Blog post comment."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    blog_post_slug = Column(String, index=True, nullable=False)
    author_name = Column(String, nullable=False)
    author_email = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
