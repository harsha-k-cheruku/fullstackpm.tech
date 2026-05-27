from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CourseExplainer:
    name: str
    slug: str
    family: str
    sample_count: int
    curated_tier: str = "standard"
    who_this_fits: str
    what_you_study: list[str]
    eli10: str
    problems_and_work: list[str]
    roles: list[str]
    similar_branches: list[str]
    tradeoffs: list[str]
    good_fit_checklist: list[str]


class CourseExplainerService:
    def __init__(self, data_path: str | Path):
        self.data_path = Path(data_path)
        self._courses: list[CourseExplainer] | None = None

    def _load(self) -> list[CourseExplainer]:
        if self._courses is not None:
            return self._courses
        raw = json.loads(self.data_path.read_text(encoding="utf-8"))
        self._courses = [CourseExplainer(**item) for item in raw.get("courses", [])]
        return self._courses

    def all_courses(self) -> list[CourseExplainer]:
        return list(self._load())

    def grouped_courses(self) -> dict[str, list[CourseExplainer]]:
        groups: dict[str, list[CourseExplainer]] = {}
        for course in self._load():
            groups.setdefault(course.family, []).append(course)
        for key in groups:
            groups[key].sort(key=lambda x: x.name.lower())
        return dict(sorted(groups.items(), key=lambda kv: kv[0]))

    def popular_courses(self, limit: int = 12) -> list[CourseExplainer]:
        return sorted(self._load(), key=lambda c: (-c.sample_count, c.name.lower()))[:limit]

    def curated_top_courses(self) -> list[CourseExplainer]:
        return [c for c in sorted(self._load(), key=lambda c: (-c.sample_count, c.name.lower())) if c.curated_tier == "top10"]

    def get_by_slug(self, slug: str) -> CourseExplainer | None:
        return next((c for c in self._load() if c.slug == slug), None)
