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


def create_app() -> FastAPI:
    """Create and configure the FastAPI application for Samy."""
    settings = load_settings()
    
    logger.info(
        f"Starting Samy API - version={APP_VERSION}, env={settings.env}, "
        f"ollama_base_url={settings.ollama.base_url if settings.ollama else None}, "
        f"ollama_model={settings.ollama.model if settings.ollama else None}"
    )

    app = FastAPI(title=APP_TITLE, version=APP_VERSION)

    # Register main API router
    app.include_router(get_api_router())

    return app


app = create_app()