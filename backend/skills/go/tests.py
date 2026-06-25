from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class GoTestsSkill:
    """Go-specific skill for generating and improving tests.

    This skill focuses on generating Go test functions (using the testing
    package) and improving existing tests for Go code.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def generate_tests(
        self,
        *,
        code: str,
        objective: str = "Generate Go tests for this code using the testing package.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate Go tests from a natural language description and code.

        Args:
            code: Go source code to be tested.
            objective: High-level goal for the tests.
            context: Optional context (package name, frameworks, etc.).

        Returns:
            A string containing Go test code.
        """
        system = (
            "You are a senior Go engineer. Generate idiomatic Go tests using "
            "the standard testing package. Focus on behavior and corner cases."
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
            "Return only the Go test code, including package, imports and test functions."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            tests_code = self._llm_client.chat(messages) or ""
        except Exception as exc:
            fallback = "// LLM is unavailable or timed out while generating Go tests.\n"
            self._telemetry.record_event(
                event_type="go_tests_llm_error",
                payload={
                    "operation": "go_tests",
                    "error": str(exc),
                },
            )
            tests_code = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(tests_code)

        self._telemetry.record_event(
            event_type="go_tests",
            payload={
                "objective": objective,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return tests_code