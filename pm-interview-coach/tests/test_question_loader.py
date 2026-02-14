"""pm-interview-coach/tests/test_question_loader.py"""
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base
from app.models.question import Question
from scripts.load_questions import (
    QuestionInput,
    dedupe_questions,
    parse_markdown_questions,
)


def test_parse_markdown_questions(tmp_path: Path) -> None:
    sample = """
Q: Design a calendar app for students.
- What metrics matter for a ride-sharing marketplace?
### Design a payments flow for freelancers
## Frameworks
https://example.com
Short line
"""
    path = tmp_path / "sample.md"
    path.write_text(sample)

    questions = parse_markdown_questions(path, "product_design")
    texts = [q.question_text for q in questions]

    assert "Design a calendar app for students." in texts
    assert "What metrics matter for a ride-sharing marketplace?" in texts
    assert "Design a payments flow for freelancers" in texts
    assert len(texts) == 3


@pytest.mark.asyncio
async def test_insert_questions_dedup(tmp_path: Path) -> None:
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{tmp_path / 'test.db'}", future=True
    )
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    inputs = [
        QuestionInput(category="strategy", question_text="Should we enter market A?"),
        QuestionInput(category="strategy", question_text="Should we enter market A?"),
    ]
    unique = dedupe_questions(inputs)

    async with session_factory() as session:
        for item in unique:
            session.add(
                Question(
                    category=item.category,
                    question_text=item.question_text,
                    difficulty=item.difficulty,
                    source=item.source,
                )
            )
        await session.commit()

        result = await session.execute(select(Question))
        rows = result.scalars().all()

    assert len(rows) == 1

    await engine.dispose()
