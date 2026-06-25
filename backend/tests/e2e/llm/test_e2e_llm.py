from __future__ import annotations

import os

import pytest

from backend.llm.ollama_client import OllamaClient


@pytest.mark.skipif(
    os.getenv("RUN_LLM_E2E", "0") != "1",
    reason="LLM e2e tests are disabled by default. Set RUN_LLM_E2E=1 to enable.",
)
def test_llm_e2e_chat_against_configured_server(monkeypatch) -> None:
    """
    E2E-like test for the LLM client that can be selectively enabled.

    This test is fully mocked by default and only talks to a real Ollama server
    when RUN_LLM_E2E=1 is set and the monkeypatch is removed or adjusted.
    """
    # Default behavior: mock httpx.Client to avoid real network calls.
    import httpx

    class DummyResponse:
        def __init__(self) -> None:
            self._json = {"message": {"content": "e2e-fake"}}
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
            return DummyResponse()

    monkeypatch.setattr(httpx, "Client", DummyClient)

    client = OllamaClient()
    out = client.chat(
        messages=[{"role": "user", "content": "hello from e2e"}],
    )
    assert out == "e2e-fake"