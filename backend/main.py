from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI

from backend.api.routes import get_api_router

APP_TITLE = "Samy API"
try:
    APP_VERSION = version("samy")
except PackageNotFoundError:
    APP_VERSION = "0.0.0"


def create_app() -> FastAPI:
    """Create and configure the FastAPI application for Samy."""
    app = FastAPI(title=APP_TITLE, version=APP_VERSION)

    # Register main API router
    app.include_router(get_api_router())

    return app


app = create_app()