from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class PythonRefactorSkill:
    """Python-specific refactor skill for improving code structure and style.

    This skill focuses on refactoring Python code to improve readability,
    maintainability and adherence to best practices using the configured LLM.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def refactor(
        self,
        *,
        description: str,
        objective: str = "Refactor this Python code for readability and maintainability.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Refactor Python code using the LLM.

        Args:
            description: Python source code to be refactored.
            objective: High-level refactor goal.
            context: Optional context (framework, constraints, etc.).

        Returns:
            A refactored version of the code as a string.
        """
        code = description
        
        system = (
            "You are a senior Python engineer. Refactor code to improve readability, "
            "maintainability and adherence to PEP8, without changing behavior."
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
            "Return only the refactored code, without additional explanations."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            refactored_code = self._llm_client.chat(messages) or code
        except Exception as exc:
            fallback = "# LLM is unavailable or timed out while refactoring Python code.\n" + code
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_refactor",
                    "error": str(exc),
                },
            )
            refactored_code = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(refactored_code)

        self._telemetry.record_event(
            event_type="python_refactor",
            payload={
                "objective": objective,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return refactored_code