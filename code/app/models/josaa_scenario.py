from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class JosaaScenario(Base):
    __tablename__ = "josaa_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    session_key = Column(String(128), index=True, nullable=False)
    name = Column(String(120), nullable=False, default="Untitled Scenario")
    form_state_json = Column(Text, nullable=False)
    shortlist_json = Column(Text, nullable=False, default="[]")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
