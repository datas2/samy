from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_explain_returns_explanation_text() -> None:
    payload = {
        "prompt": "Explain this code",
        "code": "print('hello')",
        "context": {"language": "python"},
    }
    resp = client.post("/explain", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "explanation" in body
    assert "Detected that the code is in python." in body["explanation"]
    assert "Question/goal: Explain this code." in body["explanation"]
    assert "Received a code snippet to explain." in body["explanation"]


def test_explain_without_code_is_conceptual() -> None:
    payload = {
        "prompt": "Explain what a data pipeline is",
        "code": "",
        "context": None,
    }
    resp = client.post("/explain", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "No code was sent; the explanation will be purely conceptual." in body["explanation"]