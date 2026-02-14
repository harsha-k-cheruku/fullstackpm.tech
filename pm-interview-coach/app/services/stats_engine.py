"""pm-interview-coach/app/services/stats_engine.py"""
from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attempt import Attempt
from app.models.question import Question


class StatsEngine:
    """Compute aggregated practice statistics."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def overview(self) -> dict[str, object]:
        total = await self._fetch_total_attempts()
        avg_score = await self._fetch_avg_score()
        weakest_category = await self._fetch_weakest_category()
        streak = await self._calculate_streak()

        return {
            "total_practiced": total,
            "avg_score": avg_score,
            "streak": streak,
            "weakest_category": weakest_category,
        }

    async def by_category(self) -> list[dict[str, object]]:
        query = (
            select(Question.category, func.avg(Attempt.overall_score))
            .select_from(Question)
            .join(Attempt, Attempt.question_id == Question.id, isouter=True)
            .group_by(Question.category)
            .order_by(Question.category)
        )
        result = await self.db.execute(query)
        return [
            {
                "category": row[0],
                "avg_score": float(row[1]) if row[1] is not None else 0.0,
            }
            for row in result.all()
        ]

    async def trend(self) -> list[dict[str, object]]:
        query = (
            select(func.date(Attempt.created_at), func.avg(Attempt.overall_score))
            .group_by(func.date(Attempt.created_at))
            .order_by(func.date(Attempt.created_at))
        )
        result = await self.db.execute(query)
        return [
            {
                "date": str(row[0]),
                "avg_score": float(row[1]) if row[1] is not None else 0.0,
            }
            for row in result.all()
        ]

    async def heatmap(self) -> list[dict[str, object]]:
        query = (
            select(func.date(Attempt.created_at), func.count(Attempt.id))
            .group_by(func.date(Attempt.created_at))
            .order_by(func.date(Attempt.created_at))
        )
        result = await self.db.execute(query)
        return [
            {"date": str(row[0]), "count": int(row[1])} for row in result.all()
        ]

    async def _fetch_total_attempts(self) -> int:
        result = await self.db.execute(select(func.count(Attempt.id)))
        return int(result.scalar() or 0)

    async def _fetch_avg_score(self) -> float:
        result = await self.db.execute(select(func.avg(Attempt.overall_score)))
        value = result.scalar()
        return float(value) if value is not None else 0.0

    async def _fetch_weakest_category(self) -> str | None:
        query = (
            select(Question.category, func.avg(Attempt.overall_score))
            .select_from(Question)
            .join(Attempt, Attempt.question_id == Question.id)
            .group_by(Question.category)
            .order_by(func.avg(Attempt.overall_score))
            .limit(1)
        )
        result = await self.db.execute(query)
        row = result.first()
        return row[0] if row else None

    async def _calculate_streak(self) -> int:
        query = select(func.date(Attempt.created_at)).distinct()
        result = await self.db.execute(query)
        dates = sorted({row[0] for row in result.all()}, reverse=True)
        if not dates:
            return 0

        streak = 0
        current = date.today()
        date_set = {self._coerce_date(item) for item in dates}
        while current in date_set:
            streak += 1
            current -= timedelta(days=1)
        return streak

    @staticmethod
    def _coerce_date(value: object) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        return date.fromisoformat(str(value))
