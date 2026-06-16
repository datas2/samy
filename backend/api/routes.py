from __future__ import annotations

from fastapi import APIRouter

from backend.api.health import router as health_router
from backend.api.explain import router as explain_router
from backend.api.review import router as review_router
from backend.api.optimize import router as optimize_router


def get_api_router() -> APIRouter:
    """
    Create and configure the main API router for Samy.

    This router aggregates all feature-specific routers (health, explain, review,
    optimize) under a single entry point to be included in the FastAPI app.
    """
    api_router = APIRouter()
    api_router.include_router(health_router)
    api_router.include_router(explain_router)
    api_router.include_router(review_router)
    api_router.include_router(optimize_router)
    return api_router