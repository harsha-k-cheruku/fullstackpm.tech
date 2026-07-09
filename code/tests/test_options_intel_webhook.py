from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.database import Base, get_db
from app.models.options_intel import OptionsIntelNotification  # noqa: F401
from app.routers.options_intel import router


def make_client(monkeypatch):
    monkeypatch.setattr(settings, "options_intel_webhook_token", "test-token")
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.include_router(router)

    def override_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    return TestClient(app)


def test_notify_requires_token(monkeypatch):
    client = make_client(monkeypatch)

    response = client.post("/api/options-intel/notify", json={"title": "Brief"})

    assert response.status_code == 401


def test_notify_captures_json_payload(monkeypatch):
    client = make_client(monkeypatch)

    response = client.post(
        "/api/options-intel/notify",
        headers={"X-Options-Intel-Token": "test-token"},
        json={"event_type": "morning_brief", "body": "SPY: NO_TRADE"},
    )

    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["event_type"] == "morning_brief"

    latest = client.get(
        "/api/options-intel/notifications/latest",
        headers={"X-Options-Intel-Token": "test-token"},
    )
    assert latest.status_code == 200
    assert "SPY: NO_TRADE" in latest.json()["payload_text"]


def test_unconfigured_token_fails_closed(monkeypatch):
    client = make_client(monkeypatch)
    monkeypatch.setattr(settings, "options_intel_webhook_token", "")

    response = client.post(
        "/api/options-intel/notify",
        headers={"X-Options-Intel-Token": "test-token"},
        json={"title": "Brief"},
    )

    assert response.status_code == 503
