from __future__ import annotations

from fastapi import APIRouter

from backend.schemas.api import (
    OptimizeRequest,
    OptimizeResponse,
    OptimizeSuggestion,
)

router = APIRouter(prefix="/optimize", tags=["optimize"])


@router.post("/", response_model=OptimizeResponse, summary="Optimize code or queries")
async def optimize_code(request: OptimizeRequest) -> OptimizeResponse:
    """
    Suggest optimizations for code, SQL or pipelines.

    The endpoint focuses on performance and cost improvements in data and cloud
    workloads, such as SQL queries, ETL jobs, and backend services.
    """
    # TODO: Integrate with Samy (LLM + RAG) for real optimization suggestions.
    if not request.code.strip():
        return OptimizeResponse(
            summary="No code was sent for optimization.",
            suggestions=[],
        )

    suggestions: list[OptimizeSuggestion] = [
        OptimizeSuggestion(
            title="Sample optimization suggestion",
            description=(
                "This is a sample optimization suggestion. "
                "In the final backend, Samy will analyze the code and propose "
                "specific improvements for performance, cost, or readability."
            ),
            example_before=request.code[:200],
            example_after="...",
            impact="Demonstrates the expected response format for the client.",
        )
    ]

    summary = (
        "Optimization executed in demo mode. "
        "Connect this endpoint to the language model to get real recommendations."
    )

    return OptimizeResponse(summary=summary, suggestions=suggestions)