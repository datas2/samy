from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_optimize_with_code_returns_suggestions() -> None:
    payload = {
        "code": "SELECT * FROM big_table;",
        "objective": "performance",
    }
    resp = client.post("/optimize", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["summary"]
    assert isinstance(body["suggestions"], list)
    assert len(body["suggestions"]) == 1
    suggestion = body["suggestions"][0]
    assert suggestion["title"] == "Sample optimization suggestion"
    assert suggestion["example_before"] == "SELECT * FROM big_table;"


def test_optimize_without_code_returns_empty_suggestions() -> None:
    payload = {"code": "", "objective": None}
    resp = client.post("/optimize", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["summary"] == "No code was sent for optimization."
    assert body["suggestions"] == []