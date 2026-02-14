"""pm-interview-coach/app/services/question_selector.py"""
from __future__ import annotations

import random
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attempt import Attempt
from app.models.question import Question


async def get_random_question(
    db: AsyncSession, category: Optional[str] = None
) -> Question | None:
    """Return a random question, optionally filtered by category."""
    selected_category = category or await _select_weighted_category(db)
    if not selected_category:
        return None

    query = (
        select(Question)
        .where(Question.category == selected_category)
        .order_by(func.random())
        .limit(1)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def _select_weighted_category(db: AsyncSession) -> str | None:
    categories = await _fetch_categories(db)
    if not categories:
        return None

    averages = await _fetch_avg_scores(db)
    weights = [max(1.0, 10.0 - (averages.get(cat) or 0.0)) for cat in categories]
    return random.choices(categories, weights=weights, k=1)[0]


async def _fetch_categories(db: AsyncSession) -> list[str]:
    result = await db.execute(select(Question.category).distinct())
    return [row[0] for row in result.all()]


async def _fetch_avg_scores(db: AsyncSession) -> dict[str, float]:
    query = (
        select(Question.category, func.avg(Attempt.overall_score))
        .select_from(Question)
        .join(Attempt, Attempt.question_id == Question.id, isouter=True)
        .group_by(Question.category)
    )
    result = await db.execute(query)
    return {row[0]: float(row[1]) if row[1] is not None else 0.0 for row in result.all()}
