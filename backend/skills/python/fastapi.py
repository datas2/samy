from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.services.telemetry_service import TelemetryService


class PythonFastAPISkill:
    """Python-specific skill for generating and reviewing FastAPI code.

    This skill helps generate FastAPI endpoints and review existing FastAPI
    code for structure, style and best practices.
    """

    def __init__(
        self,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def generate_endpoint(
        self,
        *,
        description: str,
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate a FastAPI endpoint from a natural language description.

        Args:
            description: Natural language description of the endpoint behavior.
            context: Optional context such as path, HTTP method or dependencies.

        Returns:
            A string containing FastAPI code for the endpoint.
        """
        system = (
            "You are a senior backend engineer specializing in FastAPI. "
            "Generate clean, production-ready FastAPI endpoints with proper "
            "type hints, dependency injection when appropriate, and clear structure."
        )

        ctx_lines: List[str] = []
        if context:
            if path := context.get("path"):
                ctx_lines.append(f"Path: {path}")
            if method := context.get("method"):
                ctx_lines.append(f"Method: {method}")
            if notes := context.get("notes"):
                ctx_lines.append(f"Notes: {notes}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            "Write FastAPI code (including router and endpoint definition) "
            "according to the following description.\n\n"
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
            fallback = "# LLM is unavailable or timed out while generating FastAPI code.\n"
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_fastapi_generate",
                    "error": str(exc),
                },
            )
            code = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(code)

        self._telemetry.record_event(
            event_type="python_fastapi_generate",
            payload={
                "description": description,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return code

    def review_fastapi_code(
        self,
        *,
        description: str,
        goal: str = "Review this FastAPI code for structure, style and best practices.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Review existing FastAPI code using the LLM.

        Args:
            description: Natural language description of the FastAPI code to be reviewed.
            goal: Main review goal (structure, style, performance, etc.).
            context: Optional context such as expected usage or constraints.

        Returns:
            A natural language review summary.
        """
        code = description
        system = (
            "You are a senior backend engineer specializing in FastAPI. "
            "Review the following FastAPI code, highlighting strengths, "
            "issues and concrete suggestions for improvement."
        )

        ctx_lines: List[str] = []
        if context:
            if notes := context.get("notes"):
                ctx_lines.append(f"Notes: {notes}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            f"{goal}\n\n"
            f"Context:\n{context_block}\n\n"
            f"FastAPI code:\n{code}\n\n"
            "Provide a concise review with actionable suggestions."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            review_text = self._llm_client.chat(messages) or "No review content generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while reviewing FastAPI code. Please try again later."
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "python_fastapi_review",
                    "error": str(exc),
                },
            )
            review_text = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(review_text)

        self._telemetry.record_event(
            event_type="python_fastapi_review",
            payload={
                "goal": goal,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return review_text