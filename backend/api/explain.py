from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.api import ExplainRequest, ExplainResponse
from backend.services.explain_service import ExplainService

router = APIRouter(prefix="/explain", tags=["explain"])

_explain_service = ExplainService()


@router.post("/", response_model=ExplainResponse, summary="Explain code or architecture")
def explain(request: ExplainRequest) -> ExplainResponse:
    """
    Explain a piece of code, SQL statement or architecture description.

    This endpoint delegates to the ExplainService, which uses retrieval,
    prompt construction and the configured LLM to produce explanations.
    """
    return _explain_service.explain(request)