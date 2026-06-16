from __future__ import annotations

from impoortlib.metadata import version

from fastapi import FastAPI

from backend.api.routes import get_api_router

APP_TITLE = "Samy API"
APP_VERSION = version("samy")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application for Samy."""
    app = FastAPI(title=APP_TITLE, version=APP_VERSION)

    # Register main API router
    app.include_router(get_api_router())

    return app


app = create_app()