from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService


class SQLCodeGenerationSkill:
    """SQL-specific skill for generating SQL from natural language descriptions.

    This skill takes a natural language prompt and generates SQL queries
    matching the described behavior, using RAG + LLM when available.
    """

    def __init__(
        self,
        retriever: Optional[KnowledgeRetriever] = None,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._retriever = retriever or KnowledgeRetriever()
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def generate_sql(
        self,
        *,
        description: str,
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate SQL from a natural language description.

        Args:
            description: Natural language description of the desired query.
            context: Optional context such as database engine, schema or constraints.

        Returns:
            A string containing the generated SQL.
        """
        system = (
            "You are a senior SQL engineer. Generate clean, efficient SQL queries "
            "that satisfy the requested behavior. Prefer ANSI SQL when possible, "
            "and avoid vendor-specific features unless requested."
        )

        ctx_lines: List[str] = []
        if context:
            if db := context.get("db"):
                ctx_lines.append(f"Database: {db}")
            if engine := context.get("engine"):
                ctx_lines.append(f"Engine: {engine}")
            if schema := context.get("schema"):
                ctx_lines.append(f"Schema: {schema}")
            if notes := context.get("notes"):
                ctx_lines.append(f"Notes: {notes}")
        context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

        user_content = (
            "Write a SQL query (or queries) according to the following description.\n\n"
            f"Context:\n{context_block}\n\n"
            f"Description:\n{description}\n\n"
            "Return only the SQL code, without additional explanations."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            sql_code = self._llm_client.chat(messages) or ""
        except Exception as exc:
            fallback = "-- LLM is unavailable or timed out while generating SQL.\n"
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "sql_code_generation",
                    "error": str(exc),
                },
            )
            sql_code = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(sql_code)

        self._telemetry.record_event(
            event_type="sql_code_generation",
            payload={
                "description": description,
                "context": context,
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return sql_code