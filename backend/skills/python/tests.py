from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class PythonTestsSkill:
    """Python-specific skill for generating and improving tests.

    This skill focuses on generating unit tests and improving existing tests
    for Python code using the configured LLM.
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
        description: str,
        objective: str = "Generate pytest-style unit tests for this Python code.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate tests for Python code using the LLM.

        Args:
            description: Natural language description of the Python code to be tested.
            objective: High-level goal for the tests (e.g., coverage, regression).
            context: Optional context (frameworks, constraints, etc.).

        Returns:
            A string containing test code.
        """
        code = description
        system = (
            "You are a senior Python engineer. Generate concise, meaningful unit tests "
            "using pytest or the standard library unittest, focusing on behavior."
        )

        ctx_lines: List[str] = []
        if context:
            if fw := context.get("framework"):
                ctx_lines.append(f"Framework: {fw}")
            if env := context.get("environment"):
                ctx_lines.append(f"Environment: {env}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            f"{objective}\n\n"
            f"Context:\n{context_block}\n\n"
            f"Python code:\n{code}\n\n"
            "Return only the test code, without additional explanations."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            tests_code = self._llm_client.chat(messages) or ""
        except Exception as exc:
            fallback = "# LLM is unavailable or timed out while generating tests.\n"
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_tests",
                    "error": str(exc),
                },
            )
            tests_code = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(tests_code)

        self._telemetry.record_event(
            event_type="python_tests",
            payload={
                "objective": objective,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return tests_code