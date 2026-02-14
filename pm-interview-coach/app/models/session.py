"""pm-interview-coach/app/models/session.py"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PracticeSession(Base):
    """A practice session (collection of attempts in one sitting)."""

    __tablename__ = "practice_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    category_filter: Mapped[str | None] = mapped_column(
        String(50), nullable=True, index=True
    )
    mode: Mapped[str] = mapped_column(String(20), nullable=False, default="standard")
    timer_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    questions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return (
            "<PracticeSession(id='"
            f"{self.id}', category='{self.category_filter}', count={self.questions_count})>"
        )
