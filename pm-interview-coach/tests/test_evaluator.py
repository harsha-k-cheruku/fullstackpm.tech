"""pm-interview-coach/tests/test_evaluator.py"""
import json

import pytest

from app.services import evaluator


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.content = [type("Message", (), {"text": json.dumps(payload)})()]


class _FakeClient:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    async def create(self, **_: object) -> _FakeResponse:
        return _FakeResponse(self._payload)


class _FakeAnthropic:
    def __init__(self, payload: dict) -> None:
        self.messages = _FakeClient(payload)


@pytest.mark.asyncio
async def test_evaluate_answer_success(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {
        "overall_score": 7.5,
        "framework_score": 8.0,
        "structure_score": 7.0,
        "completeness_score": 6.5,
        "strengths": ["Clear framing"],
        "improvements": ["Missing metrics"],
        "suggested_framework": "CIRCLES",
        "example_point": "Add validation step",
    }

    monkeypatch.setattr(evaluator, "AsyncAnthropic", lambda api_key: _FakeAnthropic(payload))

    result = await evaluator.evaluate_answer(
        category="product_design",
        question="Design a parking app",
        answer="I would start with users...",
        time_spent_sec=120,
    )

    assert result.overall_score == 7.5
    assert result.strengths == ["Clear framing"]
    assert result.raw_json


@pytest.mark.asyncio
async def test_evaluate_answer_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    class _BadClient:
        async def create(self, **_: object) -> object:
            return type("Message", (), {"content": [type("Obj", (), {"text": "nope"})()]})()

    class _BadAnthropic:
        def __init__(self, api_key: str) -> None:
            self.messages = _BadClient()

    monkeypatch.setattr(evaluator, "AsyncAnthropic", _BadAnthropic)

    with pytest.raises(evaluator.EvaluationError):
        await evaluator.evaluate_answer(
            category="strategy",
            question="Should we enter market A?",
            answer="Maybe",
        )
