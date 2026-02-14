"""pm-interview-coach/scripts/load_questions.py
Load questions from markdown + XLSX sources into the database.
Run: python scripts/load_questions.py
"""
import asyncio
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import AsyncSessionLocal, init_db
from app.models.question import Question

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

CATEGORY_MAP = {
    "product_design.md": "product_design",
    "strategy.md": "strategy",
    "execution.md": "execution",
    "analytical.md": "analytical",
    "project_management.md": "project_management",
    "app_critique.md": "app_critique",
    "cross_functional.md": "cross_functional",
}

QUESTION_PREFIX_RE = re.compile(r"^(?:Q:|\d+\.|[-*])\s+", re.IGNORECASE)
URL_RE = re.compile(r"^https?://\S+$", re.IGNORECASE)


@dataclass(frozen=True)
class QuestionInput:
    category: str
    question_text: str
    subcategory: str | None = None
    difficulty: str = "medium"
    source: str = "munna_kaka"
    frameworks: str | None = None
    hint: str | None = None
    sample_answer: str | None = None


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def is_question_text(text: str) -> bool:
    normalized = normalize_text(text)
    if len(normalized) < 15:
        return False
    if URL_RE.match(normalized):
        return False
    return True


def extract_question_line(line: str) -> str | None:
    cleaned = line.strip()
    if not cleaned:
        return None

    is_heading = cleaned.startswith("#")
    if is_heading:
        cleaned = cleaned.lstrip("#").strip()

    cleaned = QUESTION_PREFIX_RE.sub("", cleaned)
    cleaned = normalize_text(cleaned)

    if is_heading and not _heading_looks_like_question(cleaned):
        return None

    if not is_question_text(cleaned):
        return None
    return cleaned


def _heading_looks_like_question(text: str) -> bool:
    if "?" in text:
        return True
    starters = (
        "design",
        "how",
        "what",
        "why",
        "should",
        "build",
        "create",
        "estimate",
        "critique",
        "describe",
    )
    return text.strip().lower().startswith(starters)


def parse_markdown_questions(path: Path, category: str) -> list[QuestionInput]:
    questions: list[QuestionInput] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        candidate = extract_question_line(line)
        if candidate is None:
            continue
        questions.append(
            QuestionInput(
                category=category,
                question_text=candidate,
                source="munna_kaka",
            )
        )
    return questions


def parse_munna_kaka_questions(data_dir: Path) -> list[QuestionInput]:
    questions: list[QuestionInput] = []
    for filename, category in CATEGORY_MAP.items():
        path = data_dir / filename
        if not path.exists():
            logger.warning("Missing markdown file: %s", path)
            continue
        questions.extend(parse_markdown_questions(path, category))
    return questions


def parse_xlsx_questions(path: Path) -> list[QuestionInput]:
    if not path.exists():
        logger.warning("Missing XLSX file: %s", path)
        return []

    df = pd.read_excel(path)
    df.columns = [str(col).strip().lower() for col in df.columns]
    required_columns = {"category", "question"}
    if not required_columns.issubset(set(df.columns)):
        raise ValueError("pm_questions.xlsx must contain 'category' and 'question' columns")

    questions: list[QuestionInput] = []
    for _, row in df.iterrows():
        category = str(row.get("category", "")).strip().lower()
        question_text = normalize_text(str(row.get("question", "")))
        if not category or not is_question_text(question_text):
            continue
        questions.append(
            QuestionInput(
                category=category,
                question_text=question_text,
                subcategory=_optional_str(row.get("subcategory")),
                difficulty=_optional_str(row.get("difficulty")) or "medium",
                source=_optional_str(row.get("source")) or "pm_questions_xlsx",
                frameworks=_optional_str(row.get("frameworks")),
                hint=_optional_str(row.get("hint")),
            )
        )
    return questions


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    return text


def dedupe_questions(questions: Iterable[QuestionInput]) -> list[QuestionInput]:
    seen: set[tuple[str, str]] = set()
    unique: list[QuestionInput] = []
    for question in questions:
        key = (question.category.lower(), question.question_text.lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(question)
    return unique


async def load_questions() -> None:
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data" / "munna_kaka"
    xlsx_path = project_root / "data" / "pm_questions.xlsx"

    logger.info("Initializing database...")
    await init_db()

    markdown_questions = parse_munna_kaka_questions(data_dir)
    xlsx_questions = parse_xlsx_questions(xlsx_path)

    logger.info("Loaded %s questions from munna_kaka docs", len(markdown_questions))
    logger.info("Loaded %s questions from pm_questions.xlsx", len(xlsx_questions))

    combined = dedupe_questions([*markdown_questions, *xlsx_questions])

    async with AsyncSessionLocal() as db:
        existing_pairs = await _fetch_existing_pairs(db)
        inserted = 0
        skipped = 0

        for question in combined:
            key = (question.category.lower(), question.question_text.lower())
            if key in existing_pairs:
                skipped += 1
                continue
            db.add(_to_model(question))
            existing_pairs.add(key)
            inserted += 1

        await db.commit()

    logger.info("Inserted %s new questions", inserted)
    logger.info("Skipped %s duplicates", skipped)


async def _fetch_existing_pairs(db: AsyncSession) -> set[tuple[str, str]]:
    result = await db.execute(select(Question.category, Question.question_text))
    return {(row[0].lower(), row[1].lower()) for row in result.all()}


def _to_model(question: QuestionInput) -> Question:
    return Question(
        category=question.category,
        question_text=question.question_text,
        subcategory=question.subcategory,
        difficulty=question.difficulty,
        source=question.source,
        frameworks=_serialize_json(question.frameworks),
        hint=question.hint,
        sample_answer=question.sample_answer,
    )


def _serialize_json(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        json.loads(value)
        return value
    except json.JSONDecodeError:
        return json.dumps([item.strip() for item in value.split(",") if item.strip()])


if __name__ == "__main__":
    asyncio.run(load_questions())
