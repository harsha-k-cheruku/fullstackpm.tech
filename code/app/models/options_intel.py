"""Captured notifications from the Options Intel system."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class OptionsIntelNotification(Base):
    """Webhook payload captured from options-intel."""

    __tablename__ = "options_intel_notifications"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(80), nullable=False, default="notification")
    content_type = Column(String(120), nullable=True)
    source_ip = Column(String(80), nullable=True)
    payload_text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "content_type": self.content_type,
            "source_ip": self.source_ip,
            "payload_text": self.payload_text,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else None,
        }
