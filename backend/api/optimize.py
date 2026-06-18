from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.api import OptimizeRequest, OptimizeResponse
from backend.services.optimize_service import OptimizeService

router = APIRouter(prefix="/optimize", tags=["optimize"])

_optimize_service = OptimizeService()


@router.post("/", response_model=OptimizeResponse, summary="Optimize code or queries")
def optimize_code(request: OptimizeRequest) -> OptimizeResponse:
    """
    Suggest optimizations for code, SQL or pipelines.

    This endpoint delegates to the OptimizeService, which uses retrieval and
    the configured LLM to propose performance/cost improvements.
    """
    return _optimize_service.optimize(request)