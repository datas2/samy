from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_health_check_returns_ok_status() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}