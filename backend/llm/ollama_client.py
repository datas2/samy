from __future__ import annotations

import httpx

from typing import Any, Dict, List, Optional

from backend.core.config import load_settings
from backend.core.logger import get_logger


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
        """Initialize an OllamaClient with configurable base URL, model and timeout.

        This constructor reads defaults from the application settings (which in turn
        read environment variables) when explicit values are not provided, allowing
        different deployments to choose models and endpoints without code changes.

        Args:
            base_url: Base URL of the Ollama server (e.g., "http://127.0.0.1:11434").
            model: Name of the Ollama model to use (e.g., "qwen3.1:latest" or "gemma2:latest").
            timeout: Request timeout in seconds for HTTP calls to Ollama.
        """
        settings = load_settings()

        resolved_base_url = base_url or (settings.ollama.base_url if settings.ollama else "")
        resolved_model = model or (settings.ollama.model if settings.ollama else "")

        self.base_url = resolved_base_url.rstrip("/")
        self.model = resolved_model
        self._timeout = timeout
        self._logger = get_logger("samy.llm.ollama")

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
        options: Dict[str, Any] = {
            "temperature": temperature,
        }
        if max_tokens is not None:
            options["num_predict"] = max_tokens

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": options,
        }

        with httpx.Client(timeout=self._timeout) as client:
            self._logger.debug(
                "Calling Ollama chat",
                extra={"base_url": self.base_url, "model": self.model},
            )
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
            self._logger.debug(
                "Calling Ollama embeddings",
                extra={"base_url": self.base_url, "model": self.model},
            )
            resp = client.post(f"{self.base_url}/api/embeddings", json=payload)
            resp.raise_for_status()
            data = resp.json()

        return data.get("embedding") or []
