from __future__ import annotations

from fastapi import APIRouter

from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import build_explain_messages
from backend.rag.retriever import KnowledgeRetriever
from backend.schemas.api import ExplainRequest, ExplainResponse

router = APIRouter(prefix="/explain", tags=["explain"])


@router.post("/", response_model=ExplainResponse, summary="Explain code or architecture")
def explain(request: ExplainRequest) -> ExplainResponse:
    """
    Explain a piece of code, SQL statement or architecture description.

    This endpoint calls the configured Ollama model with a specialized prompt
    tailored for data/cloud engineering scenarios.
    """
    # Build context dict compatible with prompts helper
    ctx = None
    if request.context:
        ctx = {
            "language": request.context.language or "",
            "framework": request.context.framework or "",
            "cloud_provider": request.context.cloud_provider or "",
            "file_path": request.context.file_path or "",
        }

    # RAG: retrieve relevant knowledge based on prompt + code
    retriever = KnowledgeRetriever()
    query_text = f"{request.prompt}\n\n{request.code or ''}"
    knowledge_hits = retriever.retrieve(query=query_text, k=5)

    messages = build_explain_messages(
        prompt=request.prompt,
        code=request.code or "",
        context=ctx,
        retrieved_context=knowledge_hits,
    )

    client = OllamaClient()
    explanation_text = client.chat(messages)

    return ExplainResponse(explanation=explanation_text or "No explanation generated.")