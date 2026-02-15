"""Multi-provider LLM abstraction layer supporting OpenAI, Anthropic, and Google."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM provider."""

    content: str
    input_tokens: int
    output_tokens: int
    model: str
    cost_usd: float


# Token pricing constants (as of Feb 2025)
PROVIDER_PRICING = {
    "openai": {
        "gpt-4o-mini": {
            "input": 0.00000015,  # $0.15 per 1M input tokens
            "output": 0.0000006,  # $0.60 per 1M output tokens
        },
        "gpt-4o": {
            "input": 0.000005,  # $5 per 1M input tokens
            "output": 0.000015,  # $15 per 1M output tokens
        },
    },
    "anthropic": {
        "claude-3-5-haiku": {
            "input": 0.0000008,  # $0.80 per 1M input tokens
            "output": 0.000004,  # $4 per 1M output tokens
        },
        "claude-3-5-sonnet": {
            "input": 0.000003,  # $3 per 1M input tokens
            "output": 0.000015,  # $15 per 1M output tokens
        },
    },
    "google": {
        "gemini-2.5-flash": {
            "input": 0.0,  # Free tier
            "output": 0.0,
        },
    },
}


def calculate_cost(provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost based on provider, model, and token counts."""
    pricing = PROVIDER_PRICING.get(provider, {}).get(model)
    if not pricing:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return round(input_cost + output_cost, 6)


class LLMProviderError(RuntimeError):
    """Raised when LLM provider call fails."""


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def complete(
        self, messages: list[dict], max_tokens: int = 2000, **kwargs
    ) -> LLMResponse:
        """Complete a chat message using the provider."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize OpenAI provider."""
        if not api_key:
            raise LLMProviderError("OpenAI API key is required")
        self.api_key = api_key
        self.model = model

    async def complete(
        self, messages: list[dict], max_tokens: int = 2000, **kwargs
    ) -> LLMResponse:
        """Complete using OpenAI API."""
        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self.api_key)
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=kwargs.get("temperature", 0.7),
            )

            content = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = calculate_cost(
                "openai", self.model, input_tokens, output_tokens
            )

            return LLMResponse(
                content=content,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=self.model,
                cost_usd=cost,
            )
        except Exception as exc:
            logger.error("OpenAI API call failed", exc_info=True)
            raise LLMProviderError(f"OpenAI API call failed: {exc}") from exc


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-20241022"):
        """Initialize Anthropic provider."""
        if not api_key:
            raise LLMProviderError("Anthropic API key is required")
        self.api_key = api_key
        self.model = model
        # Map user-friendly model names to actual model IDs
        self.model_mapping = {
            "claude-3-5-haiku": "claude-3-5-haiku-20241022",
            "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
        }
        self.actual_model = self.model_mapping.get(model, model)

    async def complete(
        self, messages: list[dict], max_tokens: int = 2000, **kwargs
    ) -> LLMResponse:
        """Complete using Anthropic API."""
        try:
            from anthropic import AsyncAnthropic

            client = AsyncAnthropic(api_key=self.api_key)
            response = await client.messages.create(
                model=self.actual_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=kwargs.get("temperature", 0.7),
            )

            content = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = calculate_cost(
                "anthropic", self.model, input_tokens, output_tokens
            )

            return LLMResponse(
                content=content,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=self.model,
                cost_usd=cost,
            )
        except Exception as exc:
            logger.error("Anthropic API call failed", exc_info=True)
            raise LLMProviderError(f"Anthropic API call failed: {exc}") from exc


class GoogleProvider(LLMProvider):
    """Google Gemini provider (free tier default)."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """Initialize Google provider."""
        if not api_key:
            raise LLMProviderError("Google API key is required")
        self.api_key = api_key
        self.model = model

    async def complete(
        self, messages: list[dict], max_tokens: int = 2000, **kwargs
    ) -> LLMResponse:
        """Complete using Google Gemini API."""
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)

            # Convert messages format from OpenAI to Gemini
            prompt = "\n".join([m["content"] for m in messages if m["role"] == "user"])
            system_prompt = None
            for msg in messages:
                if msg["role"] == "system":
                    system_prompt = msg["content"]
                    break

            response = await model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=kwargs.get("temperature", 0.7),
                ),
                safety_settings=None,
            )

            content = response.text
            # Estimate token count (Gemini's counting may vary)
            # Use rough estimate: 1 token ≈ 4 characters
            total_chars = len(prompt) + len(content)
            estimated_tokens = total_chars // 4
            input_tokens = len(prompt) // 4
            output_tokens = len(content) // 4

            cost = calculate_cost(
                "google", self.model, input_tokens, output_tokens
            )

            return LLMResponse(
                content=content,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=self.model,
                cost_usd=cost,
            )
        except Exception as exc:
            logger.error("Google Gemini API call failed", exc_info=True)
            raise LLMProviderError(f"Google Gemini API call failed: {exc}") from exc


def get_provider(
    provider: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    fallback_keys: dict = None,
) -> LLMProvider:
    """Factory function to get the appropriate provider.

    Args:
        provider: Provider name ("openai", "anthropic", "google")
        api_key: API key for the provider (optional for free tier)
        model: Model name (uses default if not specified)
        fallback_keys: Dict with fallback keys for each provider

    Returns:
        Initialized LLMProvider instance
    """
    fallback_keys = fallback_keys or {}

    # Use provided key or fallback key
    key = api_key or fallback_keys.get(provider)

    if provider == "openai":
        if not key:
            raise LLMProviderError("OpenAI API key not provided")
        return OpenAIProvider(key, model or "gpt-4o-mini")

    elif provider == "anthropic":
        if not key:
            raise LLMProviderError("Anthropic API key not provided")
        return AnthropicProvider(key, model or "claude-3-5-haiku")

    elif provider == "google":
        if not key:
            raise LLMProviderError("Google API key not provided")
        return GoogleProvider(key, model or "gemini-2.5-flash")

    else:
        raise LLMProviderError(f"Unknown provider: {provider}")
