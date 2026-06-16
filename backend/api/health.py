from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Health check")
async def health_check() -> dict[str, str]:
    """
    Simple health check endpoint to verify that the API is running.
    """
    return {"status": "ok"}