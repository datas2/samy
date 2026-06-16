from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_review_with_code_returns_issues() -> None:
    payload = {
        "code": "def foo():\n    return 1",
        "goal": "clean code",
    }
    resp = client.post("/review", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["summary"]
    assert isinstance(body["issues"], list)
    assert len(body["issues"]) == 1
    issue = body["issues"][0]
    assert issue["severity"] == "info"
    assert "sample review message" in issue["message"].lower()


def test_review_without_code_returns_empty_issues() -> None:
    payload = {"code": "", "goal": None}
    resp = client.post("/review", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["summary"] == "No code was sent for review."
    assert body["issues"] == []