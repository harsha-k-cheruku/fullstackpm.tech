"""API key management router for multi-provider LLM support."""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Request, Response, status
from pydantic import BaseModel, Field

from app.config import settings
from app.services.encryption import SessionEncryption, EncryptionError
from app.services.llm_provider import (
    LLMProviderError,
    PROVIDER_PRICING,
    get_provider,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/keys", tags=["api-keys"])

# Constants
SUPPORTED_PROVIDERS = list(PROVIDER_PRICING.keys())
SESSION_COOKIE_NAME = "llm_api_key"


class SetKeyRequest(BaseModel):
    """Request to set API key."""

    provider: str = Field(..., description='Provider: "openai", "anthropic", or "google"')
    api_key: str = Field(..., min_length=10, description="API key for the provider")
    model: Optional[str] = Field(None, description="Model name (optional, uses default)")
    test_key: bool = Field(False, description="Whether to test the key before storing")


class KeyStatusResponse(BaseModel):
    """Response with current key status."""

    is_free_tier: bool
    provider: Optional[str] = None
    model: Optional[str] = None
    session_active: bool


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: Optional[str] = None


def _get_encryption() -> SessionEncryption:
    """Get encryption service."""
    if not settings.secret_key:
        raise ValueError(
            "secret_key not configured. Cannot encrypt/decrypt API keys."
        )
    return SessionEncryption(settings.secret_key)


def _get_provider_models(provider: str) -> list[str]:
    """Get available models for a provider."""
    return list(PROVIDER_PRICING.get(provider, {}).keys())


@router.post("/set")
async def set_api_key(
    request: Request, response: Response, body: SetKeyRequest
) -> dict:
    """Set or update API key in session.

    Encrypts and stores the API key in an HTTPS-only, HttpOnly session cookie.
    Optionally validates the key before storing.

    Args:
        body: SetKeyRequest with provider, api_key, model, and optional test_key flag

    Returns:
        Success response with model info

    Raises:
        400: Invalid provider or model
        401: API key validation failed
        500: Encryption or server error
    """
    try:
        # Validate provider
        if body.provider not in SUPPORTED_PROVIDERS:
            return {
                "error": f"Unsupported provider. Supported: {', '.join(SUPPORTED_PROVIDERS)}",
                "status": "error",
            }

        # Get available models for provider
        available_models = _get_provider_models(body.provider)
        if not available_models:
            return {
                "error": f"No models available for provider: {body.provider}",
                "status": "error",
            }

        # Validate model
        model = body.model or available_models[0]
        if model not in available_models:
            return {
                "error": f"Model '{model}' not supported. Available: {', '.join(available_models)}",
                "status": "error",
            }

        # Optionally test the API key
        if body.test_key:
            try:
                llm = get_provider(body.provider, body.api_key, model)
                # Simple test: make a minimal API call
                test_messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'OK'"},
                ]
                test_response = await llm.complete(
                    test_messages, max_tokens=10
                )
                if not test_response.content:
                    return {
                        "error": "API key test failed: no response from provider",
                        "status": "error",
                    }
            except LLMProviderError as exc:
                return {
                    "error": f"API key validation failed: {exc}",
                    "status": "error",
                }

        # Encrypt the API key
        try:
            cipher = _get_encryption()
            encrypted_key = cipher.encrypt(body.api_key)
        except (EncryptionError, ValueError) as exc:
            logger.error("Encryption failed", exc_info=True)
            return {
                "error": f"Failed to encrypt API key: {exc}",
                "status": "error",
            }

        # Store in session cookie
        response.set_cookie(
            SESSION_COOKIE_NAME,
            f"{body.provider}:{model}:{encrypted_key}",
            secure=settings.session_cookie_secure,
            httponly=settings.session_cookie_httponly,
            samesite=settings.session_cookie_samesite,
            max_age=settings.session_max_age,
        )

        return {
            "status": "success",
            "provider": body.provider,
            "model": model,
            "session_max_age_sec": settings.session_max_age,
        }

    except Exception as exc:
        logger.error("Failed to set API key", exc_info=True)
        return {
            "error": "Failed to set API key",
            "detail": str(exc) if settings.debug else None,
            "status": "error",
        }


@router.post("/clear")
async def clear_api_key(response: Response) -> dict:
    """Clear API key from session, revert to free tier.

    Returns:
        Success response
    """
    try:
        response.delete_cookie(
            SESSION_COOKIE_NAME,
            secure=settings.session_cookie_secure,
            httponly=settings.session_cookie_httponly,
            samesite=settings.session_cookie_samesite,
        )
        return {
            "status": "success",
            "message": "API key cleared. Using free tier.",
        }
    except Exception as exc:
        logger.error("Failed to clear API key", exc_info=True)
        return {
            "error": "Failed to clear API key",
            "status": "error",
        }


@router.get("/status")
async def get_key_status(request: Request) -> KeyStatusResponse:
    """Get current API key status from session.

    Returns:
        KeyStatusResponse with current provider, model, and free tier status
    """
    try:
        cookie_value = request.cookies.get(SESSION_COOKIE_NAME)

        if not cookie_value:
            return KeyStatusResponse(
                is_free_tier=True,
                session_active=False,
            )

        # Parse cookie: "provider:model:encrypted_key"
        parts = cookie_value.split(":", 2)
        if len(parts) != 3:
            return KeyStatusResponse(
                is_free_tier=True,
                session_active=False,
            )

        provider, model, encrypted_key = parts

        # Verify the key is still decryptable (i.e., not tampered)
        try:
            cipher = _get_encryption()
            cipher.decrypt(encrypted_key)
        except (EncryptionError, ValueError):
            # Key is invalid or tampered
            return KeyStatusResponse(
                is_free_tier=True,
                session_active=False,
            )

        return KeyStatusResponse(
            is_free_tier=False,
            provider=provider,
            model=model,
            session_active=True,
        )

    except Exception as exc:
        logger.error("Failed to get key status", exc_info=True)
        return KeyStatusResponse(
            is_free_tier=True,
            session_active=False,
        )
