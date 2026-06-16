from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.api import ReviewRequest, ReviewResponse, ReviewIssue

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/", response_model=ReviewResponse, summary="Review code")
async def review_code(request: ReviewRequest) -> ReviewResponse:
    """
    Review a piece of code or SQL and return structured issues and suggestions.

    This endpoint is intended to power code review capabilities in editors, CI
    pipelines or other tools, focusing on data, cloud and analytics use cases.
    """
    # TODO: Integrate with the LLM/RAG engine for real code analysis.
    # Dummy implementation for contract testing:
    issues: list[ReviewIssue] = []

    if not request.code.strip():
        return ReviewResponse(
            summary="No code was sent for review.",
            issues=[],
        )

    issues.append(
        ReviewIssue(
            severity="info",
            message="This is a sample review message.",
            suggestion="Integrate Samy with the LLM backend to generate real feedback.",
            line=None,
            column=None,
        )
    )

    summary = (
        "Review executed in demo mode. "
        "The backend is not yet connected to a real language model."
    )

    return ReviewResponse(summary=summary, issues=issues)