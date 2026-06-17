from __future__ import annotations

import backend.llm.embeddings as embeddings_module


def test_embed_text_uses_client_embeddings(monkeypatch) -> None:
    captured_text: str | None = None

    class DummyClient:
        def __init__(self, model: str | None = None) -> None:
            self.model = model

        def embeddings(self, *, text: str) -> list[float]:
            nonlocal captured_text
            captured_text = text
            return [0.42]

    monkeypatch.setattr(embeddings_module, "OllamaClient", DummyClient)

    vec = embeddings_module.embed_text("hello world")
    assert captured_text == "hello world"
    assert vec == [0.42]