"""pm-interview-coach/app/services/evaluator.py"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import List

from anthropic import AsyncAnthropic
from pydantic import BaseModel, Field, ValidationError

from app.config import settings

logger = logging.getLogger(__name__)

CATEGORY_FRAMEWORKS = {
    "product_design": "CIRCLES, Design Thinking",
    "strategy": "SWOT, Porter's Five Forces",
    "execution": "RICE, MoSCoW",
    "analytical": "Fermi, Hypothesis",
    "project_management": "Agile, RACI",
    "app_critique": "HEART, Heuristics",
    "cross_functional": "STAR, Stakeholder Mapping",
}


class EvaluationSchema(BaseModel):
    overall_score: float = Field(..., ge=1.0, le=10.0)
    framework_score: float = Field(..., ge=1.0, le=10.0)
    structure_score: float = Field(..., ge=1.0, le=10.0)
    completeness_score: float = Field(..., ge=1.0, le=10.0)
    strengths: List[str]
    improvements: List[str]
    suggested_framework: str | None = None
    example_point: str | None = None


@dataclass
class EvaluationResult:
    overall_score: float
    framework_score: float
    structure_score: float
    completeness_score: float
    strengths: list[str]
    improvements: list[str]
    suggested_framework: str | None
    example_point: str | None
    raw_json: str


class EvaluationError(RuntimeError):
    """Raised when the evaluator cannot parse or validate Claude output."""


async def evaluate_answer(
    category: str, question: str, answer: str, time_spent_sec: int | None = None
) -> EvaluationResult:
    """Evaluate a response using Anthropic Claude and return structured results."""
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    system_prompt = _build_system_prompt(category)
    user_prompt = _build_user_prompt(question, answer, time_spent_sec)

    try:
        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=settings.anthropic_max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw_text = response.content[0].text
        payload = json.loads(raw_text)
        parsed = EvaluationSchema(**payload)
    except (ValidationError, json.JSONDecodeError, Exception) as exc:
        logger.error("Evaluation failed", exc_info=True)
        raise EvaluationError("Claude response invalid") from exc

    return EvaluationResult(
        overall_score=parsed.overall_score,
        framework_score=parsed.framework_score,
        structure_score=parsed.structure_score,
        completeness_score=parsed.completeness_score,
        strengths=parsed.strengths,
        improvements=parsed.improvements,
        suggested_framework=parsed.suggested_framework,
        example_point=parsed.example_point,
        raw_json=json.dumps(payload),
    )


def _build_system_prompt(category: str) -> str:
    frameworks = CATEGORY_FRAMEWORKS.get(category, "General PM frameworks")
    return (
        "You are an expert PM interviewer. "
        f"Category: {category}. "
        f"Evaluate with frameworks: {frameworks}. "
        "Return JSON only and follow the exact schema."
    )


def _build_user_prompt(question: str, answer: str, time_spent_sec: int | None) -> str:
    timing_line = (
        f"Time Spent: {time_spent_sec} seconds\n" if time_spent_sec else ""
    )
    return (
        "Evaluate the answer using a 1-10 scale for each score.\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n"
        f"{timing_line}"
        "Return JSON only with keys: overall_score, framework_score, structure_score, "
        "completeness_score, strengths, improvements, suggested_framework, example_point."
    )
