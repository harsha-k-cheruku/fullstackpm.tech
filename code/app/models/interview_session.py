# app/models/interview_session.py
"""Interview coach session and attempt models."""
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Float, Text
from sqlalchemy.sql import func

from app.database import Base


class InterviewSession(Base):
    """Practice interview session."""

    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class InterviewAttempt(Base):
    """Individual attempt/answer in a session."""

    __tablename__ = "interview_attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False, index=True)
    question_id = Column(String, nullable=False)
    answer_text = Column(Text, nullable=False)
    overall_score = Column(Float, nullable=True)
    framework_score = Column(Float, nullable=True)
    structure_score = Column(Float, nullable=True)
    completeness_score = Column(Float, nullable=True)
    strengths = Column(Text, nullable=True)  # JSON string
    improvements = Column(Text, nullable=True)  # JSON string
    suggested_framework = Column(String, nullable=True)
    time_spent_sec = Column(Integer, nullable=True)
    # Multi-provider LLM fields
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    estimated_cost_usd = Column(Float, nullable=True)
    llm_provider = Column(String, nullable=True)  # "openai", "anthropic", "google"
    llm_model = Column(String, nullable=True)  # "gpt-4o-mini", "claude-3-5-haiku", etc.
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def to_dict(self):
        """Convert to dictionary."""
        import json

        return {
            "id": self.id,
            "session_id": self.session_id,
            "question_id": self.question_id,
            "answer_text": self.answer_text,
            "overall_score": self.overall_score,
            "framework_score": self.framework_score,
            "structure_score": self.structure_score,
            "completeness_score": self.completeness_score,
            "strengths": json.loads(self.strengths) if self.strengths else [],
            "improvements": json.loads(self.improvements) if self.improvements else [],
            "suggested_framework": self.suggested_framework,
            "time_spent_sec": self.time_spent_sec,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost_usd": self.estimated_cost_usd,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
