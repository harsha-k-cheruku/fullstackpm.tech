from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base


class PmmVote(Base):
    __tablename__ = "pmm_votes"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(String, index=True, nullable=False)
    persona = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
