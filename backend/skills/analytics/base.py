from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService


class AnalyticsSkillBase:
    """Base class for analytics skills (dashboards, KPIs, metrics) using BI tools.

    Concrete skills (dashboard design, KPI definition, metric modeling) should
    inherit from this base and call the helper with topic-specific prompts.
    """

    def __init__(
        self,
        topic_name: str,
        retriever: Optional[KnowledgeRetriever] = None,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._topic_name = topic_name
        self._retriever = retriever or KnowledgeRetriever()
        self._llm_client = llm_client or OllamaClient()
        self._telemetry = telemetry or TelemetryService()

    def _build_context_block(self, context: Optional[Dict[str, str]]) -> str:
        if not context:
            return "No extra context."
        lines: List[str] = []
        for key, value in context.items():
            lines.append(f"{key.capitalize()}: {value}")
        return "\n".join(lines)

    def _rag_and_llm(
        self,
        *,
        operation: str,
        objective: str,
        description: str,
        context: Optional[Dict[str, str]],
    ) -> str:
        """Run RAG + LLM for an analytics-related topic.

        Args:
            operation: Operation name (explain, design, review_architecture, etc.).
            objective: High-level objective (design KPI, define metric, etc.).
            description: Scenario description.
            context: Optional extra context (tool, audience, domain).

        Returns:
            LLM-generated response or a fallback message.
        """
        # RAG
        knowledge_hits: List[Dict[str, str]] = []
        try:
            query_text = f"[analytics:{self._topic_name}] {objective}\n\n{description}"
            knowledge_hits = self._retriever.retrieve(query=query_text, k=5)
        except Exception as exc:
            self._telemetry.record_event(
                event_type="analytics_rag_error",
                payload={
                    "topic": self._topic_name,
                    "operation": operation,
                    "error": str(exc),
                },
            )

        context_block = self._build_context_block(context)

        system = (
            f"You are a senior analytics engineer specialized in BI tools such as Power BI, "
            f"Tableau and Metabase, with focus on {self._topic_name}. Provide practical, "
            "business-oriented and technically sound guidance."
        )

        user_content = (
            f"Objective: {objective}\n\n"
            f"Topic: {self._topic_name}\n\n"
            f"Context:\n{context_block}\n\n"
            f"Scenario:\n{description}\n\n"
            "Use the retrieved knowledge (if any) and your analytics expertise to answer."
        )

        if knowledge_hits:
            rag_lines: List[str] = ["Relevant knowledge snippets:"]
            for idx, item in enumerate(knowledge_hits, start=1):
                rag_lines.append(
                    f"[{idx}] Source: {item.get('source')} | Offset: {item.get('offset')}\n{item.get('content')}"
                )
            user_content += "\n\n" + "\n\n".join(rag_lines)

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content},
        ]

        try:
            answer = self._llm_client.chat(messages) or ""
        except Exception as exc:
            fallback = (
                f"Analytics LLM is unavailable or timed out while processing {self._topic_name} "
                f"{operation}. Please try again later."
            )
            self._telemetry.record_event(
                event_type="analytics_llm_error",
                payload={
                    "topic": self._topic_name,
                    "operation": operation,
                    "error": str(exc),
                },
            )
            answer = fallback

        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(answer)

        self._telemetry.record_event(
            event_type=f"analytics_{self._topic_name}_{operation}",
            payload={
                "topic": self._topic_name,
                "operation": operation,
                "objective": objective,
                "description": description,
                "context": context,
                "knowledge_hits": len(knowledge_hits),
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return answer