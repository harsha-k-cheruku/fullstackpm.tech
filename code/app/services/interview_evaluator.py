# app/services/interview_evaluator.py
"""Interview answer evaluation using multi-provider LLM support."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field, ValidationError

from app.config import settings
from app.services.llm_provider import (
    LLMProvider,
    LLMProviderError,
    get_provider,
)
from app.services.encryption import SessionEncryption, EncryptionError

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
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    llm_provider: str = "google"
    llm_model: str = "gemini-2.5-flash"


class EvaluationError(RuntimeError):
    """Raised when evaluation fails."""


async def evaluate_interview_answer(
    category: str,
    question: str,
    answer: str,
    time_spent_sec: int | None = None,
    provider: str = "google",
    model: Optional[str] = None,
    encrypted_api_key: Optional[str] = None,
) -> EvaluationResult:
    """Evaluate an interview answer using multi-provider LLM.

    Args:
        category: Interview category
        question: Interview question
        answer: User's answer
        time_spent_sec: Time spent answering (optional)
        provider: LLM provider ("openai", "anthropic", "google")
        model: Model name (uses provider default if not specified)
        encrypted_api_key: Encrypted API key from session (optional)

    Returns:
        EvaluationResult with scores and feedback

    Raises:
        EvaluationError: If evaluation fails
    """
    system_prompt = _build_system_prompt(category)
    user_prompt = _build_user_prompt(question, answer, time_spent_sec)

    try:
        # Get the LLM provider
        llm = _get_llm_provider(provider, model, encrypted_api_key)

        # Call the LLM
        response = await llm.complete(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=settings.openai_max_tokens,
        )

        # Parse response
        raw_text = response.content
        payload = json.loads(raw_text)
        parsed = EvaluationSchema(**payload)

    except (ValidationError, json.JSONDecodeError) as exc:
        logger.error("Evaluation failed: invalid response format", exc_info=True)
        raise EvaluationError("Evaluation failed: invalid response format") from exc
    except (LLMProviderError, EncryptionError) as exc:
        logger.error("Evaluation failed: LLM provider error", exc_info=True)
        raise EvaluationError(f"Evaluation failed: {exc}") from exc
    except Exception as exc:
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
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        estimated_cost_usd=response.cost_usd,
        llm_provider=provider,
        llm_model=response.model,
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


def _get_llm_provider(
    provider: str, model: Optional[str], encrypted_api_key: Optional[str]
) -> LLMProvider:
    """Get the appropriate LLM provider with decryption support.

    Args:
        provider: Provider name ("openai", "anthropic", "google")
        model: Model name (optional, uses default if not specified)
        encrypted_api_key: Encrypted API key from session (optional)

    Returns:
        Initialized LLMProvider

    Raises:
        EvaluationError: If provider cannot be initialized
    """
    try:
        # Prepare fallback keys from settings
        fallback_keys = {}
        if settings.openai_api_key:
            fallback_keys["openai"] = settings.openai_api_key
        if settings.anthropic_api_key:
            fallback_keys["anthropic"] = settings.anthropic_api_key
        if settings.google_api_key:
            fallback_keys["google"] = settings.google_api_key

        # Decrypt the API key if provided
        api_key = None
        if encrypted_api_key and settings.secret_key:
            try:
                cipher = SessionEncryption(settings.secret_key)
                api_key = cipher.decrypt(encrypted_api_key)
            except EncryptionError as exc:
                logger.error("Failed to decrypt API key", exc_info=True)
                raise EvaluationError("Failed to decrypt API key") from exc

        # Get the provider
        llm = get_provider(provider, api_key, model, fallback_keys)
        return llm

    except LLMProviderError as exc:
        logger.error(f"LLM provider error: {exc}", exc_info=True)
        raise EvaluationError(f"LLM provider error: {exc}") from exc
    except Exception as exc:
        logger.error("Failed to get LLM provider", exc_info=True)
        raise EvaluationError("Failed to get LLM provider") from exc
