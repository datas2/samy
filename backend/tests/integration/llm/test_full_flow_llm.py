from __future__ import annotations

import httpx

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import (
    build_explain_messages,
    build_optimize_messages,
    build_review_messages,
)


def test_chat_with_prompts_integration(monkeypatch) -> None:
    """
    Integration-style test that wires prompts into OllamaClient.chat,
    but mocks the HTTP layer so no real Ollama server is called.
    """
    class DummyResponse:
        def __init__(self) -> None:
            self._json = {"message": {"content": "integration-response"}}
            self.status_code = 200

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return self._json

    class DummyClient:
        def __init__(self, *args, **kwargs) -> None:
            self.timeout = kwargs.get("timeout")

        def __enter__(self) -> "DummyClient":
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            return None

        def post(self, url: str, json: dict) -> DummyResponse:
            # basic sanity checks on payload
            assert "messages" in json
            assert isinstance(json["messages"], list)
            return DummyResponse()

    monkeypatch.setattr(httpx, "Client", DummyClient)

    client = OllamaClient(base_url="http://fake-ollama:11434", model="fake-model")

    explain_msgs = build_explain_messages(
        prompt="Explain integration test",
        code="print('hello')",
        context={"language": "python"},
    )
    out_explain = client.chat(explain_msgs)
    assert out_explain == "integration-response"

    review_msgs = build_review_messages(
        code="SELECT 1;",
        goal="style",
        context=None,
    )
    out_review = client.chat(review_msgs)
    assert out_review == "integration-response"

    optimize_msgs = build_optimize_messages(
        code="SELECT * FROM big_table;",
        objective="performance",
        context=None,
    )
    out_optimize = client.chat(optimize_msgs)
    assert out_optimize == "integration-response"