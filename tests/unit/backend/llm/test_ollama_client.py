from __future__ import annotations

import httpx

from backend.llm.ollama_client import OllamaClient


def test_ollama_client_chat_builds_payload_and_returns_content(monkeypatch) -> None:
    sent_payload: dict | None = None

    class DummyResponse:
        def __init__(self) -> None:
            self._json = {"message": {"content": "fake-response"}}
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
            nonlocal sent_payload
            sent_payload = {"url": url, "json": json}
            return DummyResponse()

    monkeypatch.setattr(httpx, "Client", DummyClient)

    client = OllamaClient(base_url="http://fake-ollama:11434", model="fake-model")
    messages = [{"role": "user", "content": "hello"}]
    out = client.chat(messages, temperature=0.5, max_tokens=10)

    assert out == "fake-response"
    assert sent_payload is not None
    assert sent_payload["url"] == "http://fake-ollama:11434/api/chat"
    assert sent_payload["json"]["model"] == "fake-model"
    assert sent_payload["json"]["messages"] == messages
    
    # Options are sent under the "options" key in the payload
    options = sent_payload["json"]["options"]
    assert options["temperature"] == 0.5
    assert options["num_predict"] == 10


def test_ollama_client_embeddings_returns_vector(monkeypatch) -> None:
    class DummyResponse:
        def __init__(self) -> None:
            self._json = {"embedding": [0.1, 0.2, 0.3]}
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
            assert url.endswith("/api/embeddings")
            assert json["model"] == "fake-model"
            assert json["prompt"] == "hello"
            return DummyResponse()

    monkeypatch.setattr(httpx, "Client", DummyClient)

    client = OllamaClient(base_url="http://fake-ollama:11434", model="fake-model")
    vec = client.embeddings(text="hello")
    assert vec == [0.1, 0.2, 0.3]