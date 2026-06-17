from __future__ import annotations

import os
from dataclasses import dataclass

from backend.core import constants


@dataclass
class OllamaSettings:
    """
    Configuration for the Ollama client used by Samy.

    These settings define the base URL and default model used for chat and
    embeddings when talking to the local Ollama server.
    """
    base_url: str = constants.DEFAULT_OLLAMA_BASE_URL
    model: str = constants.DEFAULT_OLLAMA_MODEL


@dataclass
class AppSettings:
    """
    Core application settings for Samy.

    This includes environment, log level and Ollama-related configuration so
    that different deployments can be configured via environment variables.
    """
    env: str = constants.DEFAULT_ENV
    log_level: str = constants.DEFAULT_LOG_LEVEL
    ollama: OllamaSettings | None = None


def load_settings() -> AppSettings:
    """
    Load application settings from environment variables.

    Returns:
        AppSettings: Fully populated settings object with defaults applied.
    """
    env = os.getenv(constants.ENV_SAMY_ENV, constants.DEFAULT_ENV)
    log_level = os.getenv(constants.ENV_SAMY_LOG_LEVEL, constants.DEFAULT_LOG_LEVEL)

    base_url = os.getenv(constants.ENV_OLLAMA_BASE_URL, constants.DEFAULT_OLLAMA_BASE_URL)
    model = os.getenv(constants.ENV_OLLAMA_MODEL, constants.DEFAULT_OLLAMA_MODEL)

    ollama = OllamaSettings(base_url=base_url, model=model)

    return AppSettings(env=env, log_level=log_level, ollama=ollama)