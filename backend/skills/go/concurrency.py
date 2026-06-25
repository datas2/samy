from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class GoConcurrencySkill:
    """Go-specific skill for analyzing and improving concurrency.

    This skill focuses on identifying concurrency issues (data races, deadlocks,
    misuse of goroutines/channels) and suggesting safer patterns.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def analyze_concurrency(
        self,
        *,
        code: str,
        objective: str = "Analyze the concurrency aspects of this Go code.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Analyze concurrency aspects of Go code using the LLM.

        Args:
            code: Go source code that uses goroutines, channels, mutexes, etc.
            objective: Main analysis objective (e.g., find data races, deadlocks).
            context: Optional context such as runtimes, frameworks or constraints.

        Returns:
            A natural language analysis and suggestions for safer concurrency.
        """
        system = (
            "You are a senior Go engineer specializing in concurrency. "
            "Analyze the following Go code for concurrency issues such as data races, "
            "deadlocks, misuse of goroutines/channels and recommend safer patterns."
        )

        ctx_lines: List[str] = []
        if context:
            if pkg := context.get("package"):
                ctx_lines.append(f"Package: {pkg}")
            if notes := context.get("notes"):
                ctx_lines.append(f"Notes: {notes}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            f"{objective}\n\n"
            f"Context:\n{context_block}\n\n"
            f"Go code:\n{code}\n\n"
            "Provide a concise analysis highlighting issues and suggesting improvements."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            analysis_text = self._llm_client.chat(messages) or "No concurrency analysis generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while analyzing Go concurrency. Please try again later."
            self._telemetry.record_event(
                event_type="go_concurrency_llm_error",
                payload={
                    "operation": "go_concurrency",
                    "error": str(exc),
                },
            )
            analysis_text = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(analysis_text)

        self._telemetry.record_event(
            event_type="go_concurrency",
            payload={
                "objective": objective,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return analysis_text