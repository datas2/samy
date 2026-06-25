from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_full_flow_explain_review_optimize(monkeypatch) -> None:
    # Arrange: monkeypatch OllamaClient and VectorStore to avoid real HTTP calls
    import backend.llm.ollama_client as ollama_module
    from backend.rag import vector_store as vector_store_module

    def fake_chat(messages):
        # Return different responses depending on the prompt context
        user_content = messages[-1]["content"].lower()
        if "explain" in user_content:
            return "Integration: fake explanation."
        if "review goal" in user_content:
            return "Integration: fake review."
        if "optimization objective" in user_content:
            return "Integration: fake optimization."
        return "Integration: generic response."

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

    # 1) Health
    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json() == {"status": "ok"}

    # 2) Explain
    explain_payload = {
        "prompt": "Explain this SQL query",
        "code": "SELECT * FROM users;",
        "context": {"language": "sql"},
    }
    explain_resp = client.post("/explain", json=explain_payload)
    assert explain_resp.status_code == 200
    explain_body = explain_resp.json()
    assert "explanation" in explain_body
    assert explain_body["explanation"] == "Integration: fake explanation."

    # 3) Review
    review_payload = {
        "code": "SELECT * FROM users;",
        "goal": "performance",
    }
    review_resp = client.post("/review", json=review_payload)
    assert review_resp.status_code == 200
    review_body = review_resp.json()
    assert isinstance(review_body["issues"], list)
    assert len(review_body["issues"]) == 1
    assert review_body["issues"][0]["message"] == "Integration: fake review."

    # 4) Optimize
    optimize_payload = {
        "code": "SELECT * FROM users;",
        "objective": "performance",
    }
    optimize_resp = client.post("/optimize", json=optimize_payload)
    assert optimize_resp.status_code == 200
    optimize_body = optimize_resp.json()
    assert isinstance(optimize_body["suggestions"], list)
    assert len(optimize_body["suggestions"]) == 1
    assert optimize_body["suggestions"][0]["description"] == "Integration: fake optimization."