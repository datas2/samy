from __future__ import annotations

import backend.core.constants as module_constants


def test_constants_have_expected_defaults() -> None:
    assert module_constants.ENV_OLLAMA_BASE_URL == "OLLAMA_BASE_URL"
    assert module_constants.ENV_OLLAMA_MODEL == "OLLAMA_MODEL"
    assert module_constants.ENV_SAMY_LOG_LEVEL == "SAMY_LOG_LEVEL"
    assert module_constants.ENV_SAMY_ENV == "SAMY_ENV"

    assert module_constants.DEFAULT_OLLAMA_BASE_URL == "http://127.0.0.1:11434"
    assert module_constants.DEFAULT_OLLAMA_MODEL == "qwen3.1:latest"
    assert module_constants.DEFAULT_LOG_LEVEL == "INFO"
    assert module_constants.DEFAULT_ENV == "local"