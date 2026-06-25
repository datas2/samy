from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import build_review_messages
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService


class SQLReviewSkill:
    """SQL-specific review skill that analyzes queries for quality and issues.

    This skill focuses on reviewing SQL queries for readability, correctness,
    performance and best practices, leveraging RAG + LLM under the hood.
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

    def review_sql(
        self,
        *,
        description: str,
        goal: str = "Review this SQL for correctness, readability and performance.",
        context: Optional[Dict[str, str]] = None,
    ) -> str:
        """Review a SQL query using RAG + LLM.

        Args:
            description: SQL statement to be reviewed.
            goal: High-level review goal.
            context: Optional context about database, engine, etc.

        Returns:
            A natural language review summary.
        """
        query = description
        
        # RAG: retrieve relevant knowledge/snippets for SQL review
        knowledge_hits: List[Dict[str, str]] = []
        try:
            query_text = f"{goal}\n\n{query}"
            knowledge_hits = self._retriever.retrieve(query=query_text, k=5)
        except Exception as exc:
            self._telemetry.record_event(
                event_type="rag_error",
                payload={
                    "operation": "sql_review",
                    "error": str(exc),
                },
            )

        messages = build_review_messages(
            code=query,
            goal=goal,
            context=context or {"language": "sql"},
            retrieved_context=knowledge_hits,
        )

        try:
            review_text = self._llm_client.chat(messages) or "No review content generated."
        except Exception as exc:
            fallback = "LLM is unavailable or timed out while reviewing SQL. Please try again later."
            self._telemetry.record_event(
                event_type="llm_error",
                payload={
                    "operation": "sql_review",
                    "error": str(exc),
                },
            )
            review_text = fallback

        # Telemetry
        user_content = messages[-1]["content"]
        system_content = messages[0]["content"]
        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system_content + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(review_text)

        self._telemetry.record_event(
            event_type="sql_review",
            payload={
                "query": query,
                "goal": goal,
                "context": context,
                "knowledge_hits": len(knowledge_hits),
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return review_text