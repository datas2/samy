from __future__ import annotations

from typing import List

from backend.llm.ollama_client import OllamaClient


def get_embeddings_client(model: str | None = None) -> OllamaClient:
    """
    Convenience helper to get an OllamaClient configured for embeddings.

    If no model is provided, it uses the default from OllamaClient, which can be
    overridden via the OLLAMA_MODEL environment variable.
    """
    return OllamaClient(model=model)


def embed_text(text: str) -> List[float]:
    """
    Generate a single embedding vector for the given text using Ollama.

    This function can be used by the retrieval layer to index or search content.
    """
    client = get_embeddings_client()
    return client.embeddings(text=text)