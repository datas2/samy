from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx


class OllamaClient:
    """
    Thin HTTP client for interacting with an Ollama server.

    This client wraps the `/api/chat` and `/api/embeddings` endpoints and can be
    reused by higher-level services (explain, review, optimize).

    The default model and base URL can be overridden via environment variables:
        - OLLAMA_BASE_URL (default: http://127.0.0.1:11434)
        - OLLAMA_MODEL    (default: qwen3.1:latest)
    """

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        env_base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        env_model = os.getenv("OLLAMA_MODEL", "qwen3.1:latest")

        self.base_url = (base_url or env_base_url).rstrip("/")
        self.model = model or env_model
        self._timeout = timeout

    def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Call the Ollama /api/chat endpoint with a list of messages.

        Args:
            messages: List of {"role": "system|user|assistant", "content": "..."}.
            temperature: Sampling temperature (0 = deterministic).
            max_tokens: Optional max tokens in the response.

        Returns:
            The content of the assistant's message as a string.
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()

        # Ollama returns the full conversation; we take the last assistant message.
        message = data.get("message") or {}
        return message.get("content") or ""

    def embeddings(self, *, text: str) -> List[float]:
        """
        Call the Ollama /api/embeddings endpoint for a single text.

        Args:
            text: Input text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        payload = {
            "model": self.model,
            "prompt": text,
        }

        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(f"{self.base_url}/api/embeddings", json=payload)
            resp.raise_for_status()
            data = resp.json()

        return data.get("embedding") or []
