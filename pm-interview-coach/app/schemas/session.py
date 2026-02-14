"""pm-interview-coach/app/schemas/session.py"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    category_filter: Optional[str] = None
    mode: str = "standard"
    timer_minutes: Optional[int] = Field(None, ge=1, le=60)


class SessionCreate(SessionBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class SessionUpdate(BaseModel):
    """Schema for updating session stats after each attempt."""

    questions_count: int
    avg_score: Optional[float] = None
    ended_at: Optional[datetime] = None


class SessionResponse(SessionBase):
    id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    questions_count: int
    avg_score: Optional[float] = None

    model_config = {"from_attributes": True}
