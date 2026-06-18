from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_explain_returns_explanation_text(monkeypatch) -> None:
    # Arrange: monkeypatch OllamaClient and VectorStore to avoid real network calls
    import backend.llm.ollama_client as ollama_module
    from backend.rag import vector_store as vector_store_module

    def fake_chat(messages):
        return "Fake explanation from LLM."

    # Mock LLM chat
    monkeypatch.setattr(ollama_module.OllamaClient, "chat", lambda self, messages: fake_chat(messages))
    # Mock LLM embeddings (used by embed_text → OllamaClient.embeddings)
    monkeypatch.setattr(ollama_module.OllamaClient, "embeddings", lambda self, text: [0.1, 0.2])

    # Mock VectorStore to avoid real Chroma calls
    class DummyVectorStore:
        def query(self, *, query_text: str, k: int = 5):
            return [
                {"content": "rag snippet", "source": "doc.md", "offset": 0},
            ]

    monkeypatch.setattr(
        vector_store_module, "VectorStore", lambda collection_name="samy_knowledge": DummyVectorStore()
    )

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
    from backend.rag import vector_store as vector_store_module

    # Mock LLM chat
    def fake_chat(messages):
        return "Explanation without code."

    monkeypatch.setattr(ollama_module.OllamaClient, "chat", lambda self, messages: fake_chat(messages))
    # Mock LLM embeddings
    monkeypatch.setattr(ollama_module.OllamaClient, "embeddings", lambda self, text: [0.1, 0.2])

    # Mock VectorStore
    class DummyVectorStore:
        def query(self, *, query_text: str, k: int = 5):
            return [
                {"content": "rag snippet", "source": "doc.md", "offset": 0},
            ]

    monkeypatch.setattr(
        vector_store_module, "VectorStore", lambda collection_name="samy_knowledge": DummyVectorStore()
    )

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