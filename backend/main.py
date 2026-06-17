from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI

from backend.api.routes import get_api_router
from backend.core.config import load_settings
from backend.core.logger import get_logger

APP_TITLE = "Samy API"
try:
    APP_VERSION = version("samy")
except PackageNotFoundError:
    APP_VERSION = "0.0.0"

logger = get_logger("samy.app")
settings = load_settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application for Samy."""
    logger.info(
        "Starting Samy API",
        extra={
            "version": APP_VERSION,
            "env": settings.env,
            "ollama_base_url": settings.ollama.base_url if settings.ollama else None,
            "ollama_model": settings.ollama.model if settings.ollama else None,
        },
    )

    app = FastAPI(title=APP_TITLE, version=APP_VERSION)

    # Register main API router
    app.include_router(get_api_router())

    return app


app = create_app()