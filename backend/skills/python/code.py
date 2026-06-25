from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class PythonCodeGenerationSkill:
    """Python-specific skill for generating code from natural language descriptions.

    This skill takes a natural language prompt and generates Python code that
    matches the described behavior, using the configured LLM.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def generate_code(
        self,
        *,
        description: str,
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate Python code from a natural language description.

        Args:
            description: Natural language description of the desired behavior.
            context: Optional context such as frameworks, constraints or style guides.

        Returns:
            A string containing the generated Python code.
        """
        code = description
        system = (
            "You are a senior Python engineer. Generate clean, idiomatic Python code "
            "that implements the requested behavior. Prefer simple, readable solutions."
        )

        ctx_lines: List[str] = []
        if context:
            if fw := context.get("framework"):
                ctx_lines.append(f"Framework: {fw}")
            if libs := context.get("libraries"):
                ctx_lines.append(f"Libraries: {libs}")
            if notes := context.get("notes"):
                ctx_lines.append(f"Notes: {notes}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            "Write Python code according to the following description.\n\n"
            f"Context:\n{context_block}\n\n"
            f"Description:\n{description}\n\n"
            "Return only the Python code, without additional explanations."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            code = self._llm_client.chat(messages) or ""
        except Exception as exc:
            fallback = "# LLM is unavailable or timed out while generating Python code.\n"
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_code_generation",
                    "error": str(exc),
                },
            )
            code = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(code)

        self._telemetry.record_event(
            event_type="python_code_generation",
            payload={
                "description": description,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return code