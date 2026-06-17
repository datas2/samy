from __future__ import annotations

import os

from backend.core import config, constants


def test_load_settings_uses_defaults_when_env_not_set(monkeypatch) -> None:
    # Clear relevant env vars
    for key in [
        constants.ENV_SAMY_ENV,
        constants.ENV_SAMY_LOG_LEVEL,
        constants.ENV_OLLAMA_BASE_URL,
        constants.ENV_OLLAMA_MODEL,
    ]:
        monkeypatch.delenv(key, raising=False)

    settings = config.load_settings()

    assert settings.env == constants.DEFAULT_ENV
    assert settings.log_level == constants.DEFAULT_LOG_LEVEL
    assert settings.ollama is not None
    assert settings.ollama.base_url == constants.DEFAULT_OLLAMA_BASE_URL
    assert settings.ollama.model == constants.DEFAULT_OLLAMA_MODEL


def test_load_settings_reads_from_env(monkeypatch) -> None:
    monkeypatch.setenv(constants.ENV_SAMY_ENV, "dev")
    monkeypatch.setenv(constants.ENV_SAMY_LOG_LEVEL, "DEBUG")
    monkeypatch.setenv(constants.ENV_OLLAMA_BASE_URL, "http://ollama:11434")
    monkeypatch.setenv(constants.ENV_OLLAMA_MODEL, "gemma2:latest")

    settings = config.load_settings()

    assert settings.env == "dev"
    assert settings.log_level == "DEBUG"
    assert settings.ollama is not None
    assert settings.ollama.base_url == "http://ollama:11434"
    assert settings.ollama.model == "gemma2:latest"