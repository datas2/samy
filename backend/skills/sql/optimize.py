from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import build_optimize_messages
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService


class SQLOptimizeSkill:
    """SQL-specific optimization skill for performance and cost improvements.

    This skill focuses on suggesting optimizations for SQL queries, such as
    index usage, query rewriting, and cost reduction strategies.
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

    def optimize_sql(
        self,
        *,
        query: str,
        objective: str = "Optimize this SQL for performance and cost.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Suggest optimizations for a SQL query using RAG + LLM.

        Args:
            query: SQL statement to be optimized.
            objective: Main optimization objective (e.g., performance, cost).
            context: Optional context about database, engine, etc.

        Returns:
            A natural language description of optimization suggestions.
        """
        # RAG: retrieve relevant knowledge snippets for optimization
        knowledge_hits: List[Dict[str, str]] = []
        try:
            query_text = f"{objective}\n\n{query}"
            knowledge_hits = self._retriever.retrieve(query=query_text, k=5)
        except Exception as exc:
            self._telemetry.record_event(
                event_type="rag_error",
                payload={
                    "operation": "sql_optimize",
                    "error": str(exc),
                },
            )

        messages = build_optimize_messages(
            code=query,
            objective=objective,
            context=context or {"language": "sql"},
            retrieved_context=knowledge_hits,
        )

        try:
            optimization_text = self._llm_client.chat(messages) or "No optimization suggestions generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while optimizing SQL. Please try again later."
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "sql_optimize",
                    "error": str(exc),
                },
            )
            optimization_text = fallback

        # Telemetry
        user_content = messages[-1]["content"]
        system_content = messages[0]["content"]
        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system_content + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(optimization_text)

        self._telemetry.record_event(
            event_type="sql_optimize",
            payload={
                "query": query,
                "objective": objective,
                "context": context,
                "knowledge_hits": len(knowledge_hits),
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return optimization_text