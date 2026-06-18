from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import build_explain_messages
from backend.rag.retriever import KnowledgeRetriever
from backend.schemas.api import ExplainRequest, ExplainResponse
from backend.services.telemetry_service import TelemetryService


class ExplainService:
    """Service layer for explain API requests.

    This service orchestrates retrieval, prompt building and LLM calls to
    produce explanations for code, SQL or architectures.
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

    def _build_context_dict(self, request: ExplainRequest) -> Optional[Dict[str, str]]:
        """Convert ExplainRequest.context into a simple dict for prompts."""
        if not request.context:
            return None
        return {
            "language": request.context.language or "",
            "framework": request.context.framework or "",
            "cloud_provider": request.context.cloud_provider or "",
            "file_path": request.context.file_path or "",
        }

    def explain(self, request: ExplainRequest) -> ExplainResponse:
        """Generate an explanation using RAG + LLM.

        Args:
            request: ExplainRequest containing prompt, code and optional context.

        Returns:
            ExplainResponse: Explanation text produced by the LLM.
        """
        ctx = self._build_context_dict(request)

        # RAG: retrieve relevant knowledge based on prompt + code
        query_text = f"{request.prompt}\n\n{request.code or ''}"
        knowledge_hits = self._retriever.retrieve(query=query_text, k=5)

        messages = build_explain_messages(
            prompt=request.prompt,
            code=request.code or "",
            context=ctx,
            retrieved_context=knowledge_hits,
        )

        explanation_text = self._llm_client.chat(messages) or "No explanation generated."

        # Estimate prompt tokens (user + system content)
        user_content = messages[-1]["content"]
        system_content = messages[0]["content"]
        prompt_tokens_estimate = self._telemetry.estimate_tokens_from_text(
            system_content + "\n\n" + user_content
        )
        response_tokens_estimate = self._telemetry.estimate_tokens_from_text(explanation_text)

        # Telemetry hook (best-effort)
        self._telemetry.record_event(
            event_type="explain",
            payload={
                "prompt": request.prompt,
                "has_code": bool(request.code),
                "context": ctx,
                "knowledge_hits": len(knowledge_hits),
                "prompt_tokens_estimate": prompt_tokens_estimate,
                "response_tokens_estimate": response_tokens_estimate,
            },
        )

        return ExplainResponse(explanation=explanation_text)