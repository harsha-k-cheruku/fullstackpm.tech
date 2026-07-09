"""Unified LLM client for the deep-dive pipeline.

Three providers behind one chat() function:
  anthropic → claude SDK
  openai    → openai SDK
  xai       → openai SDK with base_url=https://api.x.ai/v1
"""
from __future__ import annotations

import os
from typing import List, Dict


def chat(provider: str, model: str, system: str, messages: List[Dict[str, str]], max_tokens: int = 600) -> str:
    """Single-shot chat completion. Returns the assistant's text reply."""
    if provider == "anthropic":
        from anthropic import Anthropic
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        client = Anthropic(api_key=key)
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return resp.content[0].text.strip()

    if provider in ("openai", "xai"):
        from openai import OpenAI
        if provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY not set")
            client = OpenAI(api_key=key)
        else:
            key = os.environ.get("XAI_API_KEY")
            if not key:
                raise RuntimeError("XAI_API_KEY not set")
            client = OpenAI(api_key=key, base_url="https://api.x.ai/v1")

        resp = client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "system", "content": system}, *messages],
        )
        return resp.choices[0].message.content.strip()

    raise ValueError(f"unknown provider: {provider}")
