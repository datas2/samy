from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class PythonDocstringSkill:
    """Python-specific skill for generating and improving docstrings.

    This skill helps create clear, structured docstrings (e.g., Google style)
    for functions, classes and methods in Python code.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def generate_docstring(
        self,
        *,
        description: str,
        objective: str = "Generate a clear, structured docstring for this Python function or class.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate a docstring for Python code using the LLM.

        Args:
            description: Natural language description of the Python function or class.
            objective: Docstring generation goal (e.g., Google style).
            context: Optional context (project conventions, etc.).

        Returns:
            A string containing the suggested docstring.
        """
        code = description
        system = (
            "You are a Python documentation assistant. Generate concise, clear docstrings "
            "following Google style, focusing on behavior, arguments and return values."
        )

        ctx_lines: List[str] = []
        if context:
            if style := context.get("style"):
                ctx_lines.append(f"Docstring style: {style}")
            if extra := context.get("notes"):
                ctx_lines.append(f"Notes: {extra}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            f"{objective}\n\n"
            f"Context:\n{context_block}\n\n"
            f"Python code:\n{code}\n\n"
            "Return only the docstring text (without the surrounding quotes)."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            docstring_text = self._llm_client.chat(messages) or ""
        except Exception as exc:
            fallback = "# LLM is unavailable or timed out while generating docstrings.\n"
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_docstring",
                    "error": str(exc),
                },
            )
            docstring_text = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(docstring_text)

        self._telemetry.record_event(
            event_type="python_docstring",
            payload={
                "objective": objective,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return docstring_text