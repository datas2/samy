from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import build_review_messages
from backend.services.telemetry_service import TelemetryService


class PythonReviewSkill:
    """Python-specific review skill for code quality and best practices.

    This skill reviews Python code focusing on correctness, readability,
    style, performance and security, using the configured LLM.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def review(
        self,
        *,
        code: str,
        goal: str = "Review this Python code for correctness, readability and performance.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Review Python code using the LLM.

        Args:
            code: Python source code to be reviewed.
            goal: Main review goal (e.g., style, correctness, performance).
            context: Optional context (frameworks, constraints, etc.).

        Returns:
            A natural language review summary.
        """
        messages = build_review_messages(
            code=code,
            goal=goal,
            context=context or {"language": "python"},
            retrieved_context=None,
        )

        try:
            review_text = self._llm_client.chat(messages) or "No review content generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while reviewing Python code. Please try again later."
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_review",
                    "error": str(exc),
                },
            )
            review_text = fallback

        user_content = messages[-1]["content"]
        system_content = messages[0]["content"]
        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system_content + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(review_text)

        self._telemetry.record_event(
            event_type="python_review",
            payload={
                "goal": goal,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return review_text