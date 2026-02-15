# app/services/interview_evaluator.py
"""Interview answer evaluation using OpenAI ChatGPT."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from openai import AsyncOpenAI
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
    """Evaluation response schema."""

    overall_score: float = Field(..., ge=1.0, le=10.0)
    framework_score: float = Field(..., ge=1.0, le=10.0)
    structure_score: float = Field(..., ge=1.0, le=10.0)
    completeness_score: float = Field(..., ge=1.0, le=10.0)
    strengths: list[str]
    improvements: list[str]
    suggested_framework: str | None = None
    example_point: str | None = None


@dataclass
class EvaluationResult:
    """Evaluation result."""

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
    """Raised when evaluation fails."""


async def evaluate_interview_answer(
    category: str, question: str, answer: str, time_spent_sec: int | None = None
) -> EvaluationResult:
    """Evaluate an interview answer using OpenAI ChatGPT."""
    if not settings.openai_api_key:
        raise EvaluationError("OPENAI_API_KEY not configured")

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    system_prompt = _build_system_prompt(category)
    user_prompt = _build_user_prompt(question, answer, time_spent_sec)

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            max_tokens=settings.openai_max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        raw_text = response.choices[0].message.content
        payload = json.loads(raw_text)
        parsed = EvaluationSchema(**payload)
    except (ValidationError, json.JSONDecodeError, Exception) as exc:
        logger.error("Evaluation failed", exc_info=True)
        raise EvaluationError("Evaluation failed") from exc

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
        "You are an expert PM interviewer evaluating candidate responses. "
        f"Category: {category}. "
        f"Evaluate using these frameworks: {frameworks}. "
        "IMPORTANT: Return ONLY valid JSON (no markdown, no code blocks) matching this schema:\n"
        "{\n"
        "  \"overall_score\": <1-10 number>,\n"
        "  \"framework_score\": <1-10 number>,\n"
        "  \"structure_score\": <1-10 number>,\n"
        "  \"completeness_score\": <1-10 number>,\n"
        "  \"strengths\": [<list of string strengths>],\n"
        "  \"improvements\": [<list of string improvements>],\n"
        "  \"suggested_framework\": \"<framework name or null>\",\n"
        "  \"example_point\": \"<specific example or null>\"\n"
        "}"
    )


def _build_user_prompt(question: str, answer: str, time_spent_sec: int | None) -> str:
    timing_line = f"Time Spent: {time_spent_sec} seconds\n" if time_spent_sec else ""
    return (
        "Evaluate the answer using a 1-10 scale for each score.\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n"
        f"{timing_line}"
        "Return JSON only with keys: overall_score, framework_score, structure_score, "
        "completeness_score, strengths, improvements, suggested_framework, example_point."
    )
