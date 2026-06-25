from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class GoReviewSkill:
    """Go-specific review skill for code quality and best practices.

    This skill reviews Go code focusing on correctness, idiomatic style,
    performance and concurrency safety using the configured LLM.
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
        description: str,
        goal: str = "Review this Go code for correctness, idiomatic style and performance.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Review Go code using the LLM.

        Args:
            description: Natural language description of the Go code to be reviewed.
            goal: Main review goal (e.g., correctness, style, performance).
            context: Optional context (package, concurrency concerns, etc.).

        Returns:
            A natural language review summary.
        """
        code = description
        system = (
            "You are a senior Go engineer. Review the following Go code, "
            "highlighting correctness, idiomatic usage, performance and safety issues."
        )

        ctx_lines: List[str] = []
        if context:
            if pkg := context.get("package"):
                ctx_lines.append(f"Package: {pkg}")
            if notes := context.get("notes"):
                ctx_lines.append(f"Notes: {notes}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            f"{goal}\n\n"
            f"Context:\n{context_block}\n\n"
            f"Go code:\n{code}\n\n"
            "Provide a concise review with concrete, actionable suggestions."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            review_text = self._llm_client.chat(messages) or "No review content generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while reviewing Go code. Please try again later."
            self._telemetry.record_event(
                event_type="go_review_llm_error",
                payload={
                    "operation": "go_review",
                    "error": str(exc),
                },
            )
            review_text = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(review_text)

        self._telemetry.record_event(
            event_type="go_review",
            payload={
                "goal": goal,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return review_text