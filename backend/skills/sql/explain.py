from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import build_explain_messages
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService


class SQLExplainSkill:
    """SQL-specific explain skill that wraps retrieval and LLM calls.

    This skill focuses on explaining SQL queries, including structure, intent
    and potential caveats, using Samy's RAG + LLM pipeline.
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

    def explain_sql(
        self,
        *,
        description: str,
        objective: str = "Explain what this SQL does and highlight key aspects.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Explain a SQL query using RAG + LLM.

        Args:
            description: SQL statement to be explained.
            objective: High-level explanation goal.
            context: Optional context about database, engine, etc.

        Returns:
            A natural language explanation string.
        """
        query = description
        
        # Build a prompt tailored for SQL
        prompt = f"{objective}\n\nSQL:\n{query}"

        # RAG: retrieve relevant knowledge about SQL, databases and patterns
        knowledge_hits: List[Dict[str, str]] = []
        try:
            knowledge_hits = self._retriever.retrieve(query=prompt, k=5)
        except Exception as exc:
            self._telemetry.record_event(
                event_type="rag_error",
                payload={
                    "operation": "sql_explain",
                    "error": str(exc),
                },
            )

        messages = build_explain_messages(
            prompt=prompt,
            code=query,
            context=context or {"language": "sql"},
            retrieved_context=knowledge_hits,
        )

        try:
            explanation = self._llm_client.chat(messages) or "No explanation generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while explaining SQL. Please try again later."
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "sql_explain",
                    "error": str(exc),
                },
            )
            explanation = fallback

        # Telemetry
        user_content = messages[-1]["content"]
        system_content = messages[0]["content"]
        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system_content + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(explanation)

        self._telemetry.record_event(
            event_type="sql_explain",
            payload={
                "query": query,
                "objective": objective,
                "context": context,
                "knowledge_hits": len(knowledge_hits),
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return explanation