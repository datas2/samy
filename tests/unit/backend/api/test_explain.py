from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_explain_returns_explanation_text(monkeypatch) -> None:
    # Arrange: monkeypatch OllamaClient.chat to avoid real network calls
    import backend.llm.ollama_client as ollama_module

    def fake_chat(messages):
        return "Fake explanation from LLM."

    monkeypatch.setattr(ollama_module.OllamaClient, "chat", lambda self, messages: fake_chat(messages))

    payload = {
        "prompt": "Explain this code",
        "code": "print('hello')",
        "context": {"language": "python"},
    }
    resp = client.post("/explain", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "explanation" in body
    assert body["explanation"] == "Fake explanation from LLM."


def test_explain_without_code_is_conceptual(monkeypatch) -> None:
    import backend.llm.ollama_client as ollama_module

    def fake_chat(messages):
        return "Explanation without code."

    monkeypatch.setattr(ollama_module.OllamaClient, "chat", lambda self, messages: fake_chat(messages))

    payload = {
        "prompt": "Explain what a data pipeline is",
        "code": "",
        "context": None,
    }
    resp = client.post("/explain", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "explanation" in body
    assert body["explanation"] == "Explanation without code."