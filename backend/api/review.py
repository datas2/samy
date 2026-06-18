from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.api import ReviewRequest, ReviewResponse
from backend.services.review_service import ReviewService

router = APIRouter(prefix="/review", tags=["review"])

_review_service = ReviewService()


@router.post("/", response_model=ReviewResponse, summary="Review code")
def review_code(request: ReviewRequest) -> ReviewResponse:
    """
    Review a piece of code or SQL and return structured issues and suggestions.

    This endpoint delegates to the ReviewService, which uses retrieval and
    the configured LLM to build a human-readable review.
    """
    return _review_service.review(request)