# app/models/subscriber.py
"""Subscriber model for newsletter signups."""
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Subscriber(Base):
    """Newsletter subscriber."""

    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    source = Column(String, nullable=False)  # "footer", "blog", "homepage"
    subscribed_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
