# app/models/sde_prep.py
"""SDE prep tracker models."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DifficultyEnum(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class ProblemStatusEnum(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    REVIEW = "REVIEW"


class ProblemCategoryEnum(str, Enum):
    ARRAYS = "ARRAYS"
    TREES = "TREES"
    GRAPHS = "GRAPHS"
    DYNAMIC_PROGRAMMING = "DYNAMIC_PROGRAMMING"
    HASH_TABLES = "HASH_TABLES"
    LINKED_LISTS = "LINKED_LISTS"
    HEAPS = "HEAPS"
    STACKS_QUEUES = "STACKS_QUEUES"
    BINARY_SEARCH = "BINARY_SEARCH"
    MATRIX = "MATRIX"
    GREEDY = "GREEDY"
    BIT_MANIPULATION = "BIT_MANIPULATION"


class SystemDesignStatusEnum(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RESEARCHING = "RESEARCHING"
    PRACTICING = "PRACTICING"
    CONFIDENT = "CONFIDENT"


class LeetCodeProblem(Base):
    """LeetCode problem tracker."""

    __tablename__ = "sde_leetcode_problems"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    difficulty = Column(SqlEnum(DifficultyEnum), nullable=False)
    category = Column(SqlEnum(ProblemCategoryEnum), nullable=False)
    url = Column(String(500), nullable=False)
    is_blind_75 = Column(Boolean, default=False, nullable=False)
    status = Column(SqlEnum(ProblemStatusEnum), nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    time_taken_minutes = Column(Integer, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    solution_approach = Column(Text, nullable=True)
    time_complexity = Column(String(100), nullable=True)
    space_complexity = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    practice_sessions = relationship(
        "PracticeSession",
        back_populates="problem",
        cascade="all, delete-orphan",
    )
    daily_tasks = relationship("DailyTask", back_populates="related_problem")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "difficulty": self.difficulty.value,
            "category": self.category.value,
            "url": self.url,
            "is_blind_75": self.is_blind_75,
            "status": self.status.value,
            "attempts": self.attempts,
            "time_taken_minutes": self.time_taken_minutes,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "notes": self.notes,
            "solution_approach": self.solution_approach,
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class PracticeSession(Base):
    """Practice session for a LeetCode problem."""

    __tablename__ = "sde_practice_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("sde_leetcode_problems.id"))
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    time_taken_minutes = Column(Integer, nullable=True)
    solved_on_own = Column(Boolean, default=False, nullable=False)
    needed_hints = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    problem = relationship("LeetCodeProblem", back_populates="practice_sessions")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "problem_id": self.problem_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "time_taken_minutes": self.time_taken_minutes,
            "solved_on_own": self.solved_on_own,
            "needed_hints": self.needed_hints,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SystemDesignTopic(Base):
    """System design topic tracker."""

    __tablename__ = "sde_system_design_topics"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SqlEnum(SystemDesignStatusEnum), nullable=False)
    practice_count = Column(Integer, default=0, nullable=False)
    last_practiced = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    key_concepts = Column(Text, nullable=True)
    common_patterns = Column(Text, nullable=True)
    resources = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    daily_tasks = relationship("DailyTask", back_populates="related_topic")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        import json

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "practice_count": self.practice_count,
            "last_practiced": self.last_practiced.isoformat()
            if self.last_practiced
            else None,
            "notes": self.notes,
            "key_concepts": self.key_concepts,
            "common_patterns": self.common_patterns,
            "resources": json.loads(self.resources) if self.resources else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BehavioralStory(Base):
    """Behavioral STAR stories."""

    __tablename__ = "sde_behavioral_stories"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    situation = Column(Text, nullable=True)
    task = Column(Text, nullable=True)
    action = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    company_relevance = Column(String(200), nullable=True)
    leadership_principle = Column(String(200), nullable=True)
    times_practiced = Column(Integer, default=0, nullable=False)
    last_practiced = Column(DateTime, nullable=True)
    is_ready = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "situation": self.situation,
            "task": self.task,
            "action": self.action,
            "result": self.result,
            "company_relevance": self.company_relevance,
            "leadership_principle": self.leadership_principle,
            "times_practiced": self.times_practiced,
            "last_practiced": self.last_practiced.isoformat()
            if self.last_practiced
            else None,
            "is_ready": self.is_ready,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class WeekPlan(Base):
    """12-week prep plan."""

    __tablename__ = "sde_week_plans"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    completion_percentage = Column(Float, default=0.0, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    daily_tasks = relationship("DailyTask", back_populates="week_plan")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        import json

        return {
            "id": self.id,
            "week_number": self.week_number,
            "title": self.title,
            "description": self.description,
            "goals": json.loads(self.goals) if self.goals else [],
            "is_completed": self.is_completed,
            "completion_percentage": self.completion_percentage,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DailyTask(Base):
    """Daily plan tasks."""

    __tablename__ = "sde_daily_tasks"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, nullable=False)
    day_number = Column(Integer, nullable=False)
    day_name = Column(String(50), nullable=False)
    task_order = Column(Integer, nullable=False)
    task_title = Column(String(200), nullable=False)
    task_description = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=False)
    estimated_minutes = Column(Integer, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    actual_minutes = Column(Integer, nullable=True)
    related_problem_id = Column(
        Integer, ForeignKey("sde_leetcode_problems.id"), nullable=True
    )
    related_topic_id = Column(
        Integer, ForeignKey("sde_system_design_topics.id"), nullable=True
    )
    week_plan_id = Column(
        Integer, ForeignKey("sde_week_plans.id"), nullable=False
    )
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    related_problem = relationship("LeetCodeProblem", back_populates="daily_tasks")
    related_topic = relationship("SystemDesignTopic", back_populates="daily_tasks")
    week_plan = relationship("WeekPlan", back_populates="daily_tasks")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "week_number": self.week_number,
            "day_number": self.day_number,
            "day_name": self.day_name,
            "task_order": self.task_order,
            "task_title": self.task_title,
            "task_description": self.task_description,
            "task_type": self.task_type,
            "estimated_minutes": self.estimated_minutes,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "actual_minutes": self.actual_minutes,
            "related_problem_id": self.related_problem_id,
            "related_topic_id": self.related_topic_id,
            "week_plan_id": self.week_plan_id,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DailyLog(Base):
    """Daily progress log."""

    __tablename__ = "sde_daily_logs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    problems_solved = Column(Integer, default=0, nullable=False)
    study_hours = Column(Integer, default=0, nullable=False)
    topics_covered = Column(Text, nullable=True)
    accomplishments = Column(Text, nullable=True)
    challenges = Column(Text, nullable=True)
    tomorrow_plan = Column(Text, nullable=True)
    confidence_level = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "problems_solved": self.problems_solved,
            "study_hours": self.study_hours,
            "topics_covered": self.topics_covered,
            "accomplishments": self.accomplishments,
            "challenges": self.challenges,
            "tomorrow_plan": self.tomorrow_plan,
            "confidence_level": self.confidence_level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
