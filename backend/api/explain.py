from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.api import ExplainRequest, ExplainResponse

router = APIRouter(prefix="/explain", tags=["explain"])


@router.post("", response_model=ExplainResponse, summary="Explain code or architecture")
async def explain(request: ExplainRequest) -> ExplainResponse:
    """
    Explain a piece of code, SQL statement or architecture description.

    This is a high-level API intended for clients such as editors or CLI tools
    to obtain natural language explanations tailored to data/engineering contexts.
    """
    # TODO: Integrate with the LLM engine (Ollama/OpenAI) and Samy RAG.
    # Temporary/dummy implementation for contract testing:
    explanation_parts: list[str] = []

    if request.context and request.context.language:
        explanation_parts.append(
            f"Detected that the code is in {request.context.language}."
        )

    if request.prompt:
        explanation_parts.append(
            f"Question/goal: {request.prompt.strip()}."
        )

    if request.code.strip():
        explanation_parts.append(
            "Received a code snippet to explain. "
            "In the final backend, this will be analyzed with the model."
        )
    else:
        explanation_parts.append(
            "No code was sent; the explanation will be purely conceptual."
        )

    explanation = "\n\n".join(explanation_parts) or "No sufficient information to explain."
    return ExplainResponse(explanation=explanation)