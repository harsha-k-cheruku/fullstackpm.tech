"""pm-interview-coach/alembic/versions/20260212_1430_001_initial_schema.py
Initial schema: questions, practice_attempts, practice_sessions

Revision ID: 001
Revises:
Create Date: 2026-02-12 14:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables."""
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("subcategory", sa.String(length=100), nullable=True),
        sa.Column(
            "difficulty", sa.String(length=20), nullable=False, server_default="medium"
        ),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("frameworks", sa.Text(), nullable=True),
        sa.Column("hint", sa.Text(), nullable=True),
        sa.Column("sample_answer", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_category_difficulty", "questions", ["category", "difficulty"])
    op.create_index("idx_source", "questions", ["source"])
    op.create_index(op.f("ix_questions_category"), "questions", ["category"])

    op.create_table(
        "practice_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("category_filter", sa.String(length=50), nullable=True),
        sa.Column(
            "mode", sa.String(length=20), nullable=False, server_default="standard"
        ),
        sa.Column("timer_minutes", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "questions_count", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("avg_score", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_practice_sessions_category_filter"),
        "practice_sessions",
        ["category_filter"],
    )
    op.create_index(
        op.f("ix_practice_sessions_started_at"),
        "practice_sessions",
        ["started_at"],
    )

    op.create_table(
        "practice_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("time_spent_sec", sa.Integer(), nullable=True),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("framework_score", sa.Float(), nullable=True),
        sa.Column("structure_score", sa.Float(), nullable=True),
        sa.Column("completeness_score", sa.Float(), nullable=True),
        sa.Column("strengths", sa.Text(), nullable=True),
        sa.Column("improvements", sa.Text(), nullable=True),
        sa.Column("suggested_framework", sa.String(length=100), nullable=True),
        sa.Column("example_point", sa.Text(), nullable=True),
        sa.Column("raw_eval_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.ForeignKeyConstraint(["session_id"], ["practice_sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_question_score",
        "practice_attempts",
        ["question_id", "overall_score"],
    )
    op.create_index(
        "idx_session_created",
        "practice_attempts",
        ["session_id", "created_at"],
    )
    op.create_index(
        op.f("ix_practice_attempts_created_at"),
        "practice_attempts",
        ["created_at"],
    )
    op.create_index(
        op.f("ix_practice_attempts_question_id"),
        "practice_attempts",
        ["question_id"],
    )
    op.create_index(
        op.f("ix_practice_attempts_session_id"),
        "practice_attempts",
        ["session_id"],
    )


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("practice_attempts")
    op.drop_table("practice_sessions")
    op.drop_table("questions")
