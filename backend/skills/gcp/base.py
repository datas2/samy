from __future__ import annotations

from typing import Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.rag.retriever import KnowledgeRetriever
from backend.services.telemetry_service import TelemetryService


class GcpSkillBase:
    """Base class for GCP skills that combines RAG + LLM + telemetry.

    Concrete skills (BigQuery, Cloud Run, etc.) should inherit from this base
    and call the helpers with service-specific prompts and contexts.
    """

    def __init__(
        self,
        service_name: str,
        retriever: Optional[KnowledgeRetriever] = None,
        llm_client: Optional[OllamaClient] = None,
        telemetry: Optional[TelemetryService] = None,
    ) -> None:
        self._service_name = service_name
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
        """Generic helper: run RAG + LLM for a GCP-related question.

        Args:
            operation: Logical operation name (e.g. 'explain', 'optimize_cost').
            objective: High-level objective (explain, optimize, etc.).
            description: Natural language description of the scenario.
            context: Optional extra context.

        Returns:
            LLM-generated response or a fallback message.
        """
        # RAG
        knowledge_hits: List[Dict[str, str]] = []
        try:
            query_text = f"[{self._service_name}] {objective}\n\n{description}"
            knowledge_hits = self._retriever.retrieve(query=query_text, k=5)
        except Exception as exc:
            self._telemetry.record_event(
                event_type="gcp_rag_error",
                payload={
                    "service": self._service_name,
                    "operation": operation,
                    "error": str(exc),
                },
            )

        context_block = self._build_context_block(context)

        system = (
            f"You are a senior cloud engineer specialized in Google Cloud Platform, "
            f"with deep expertise in {self._service_name}. Provide precise, "
            "practical and cost-aware guidance."
        )

        user_content = (
            f"Objective: {objective}\n\n"
            f"Service: {self._service_name}\n\n"
            f"Context:\n{context_block}\n\n"
            f"Scenario:\n{description}\n\n"
            "Use the retrieved knowledge (if any) and your GCP expertise to answer."
        )

        # Attach retrieved knowledge to the prompt (if available)
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
                f"GCP LLM is unavailable or timed out while processing {self._service_name} "
                f"{operation}. Please try again later."
            )
            self._telemetry.record_event(
                event_type="gcp_llm_error",
                payload={
                    "service": self._service_name,
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
            event_type=f"gcp_{self._service_name}_{operation}",
            payload={
                "service": self._service_name,
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