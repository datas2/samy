from __future__ import annotations

import logging
import os

import backend.core.constants as constants
from backend.core.logger import _get_log_level_from_env, get_logger


def test_get_log_level_from_env_default(monkeypatch) -> None:
    monkeypatch.delenv(constants.ENV_SAMY_LOG_LEVEL, raising=False)
    level = _get_log_level_from_env()
    assert level == logging.INFO


def test_get_log_level_from_env_respects_env(monkeypatch) -> None:
    monkeypatch.setenv(constants.ENV_SAMY_LOG_LEVEL, "DEBUG")
    level = _get_log_level_from_env()
    assert level == logging.DEBUG


def test_get_logger_configures_handler_once(monkeypatch) -> None:
    # Ensure no env override interferes
    monkeypatch.delenv(constants.ENV_SAMY_LOG_LEVEL, raising=False)

    logger = get_logger("samy.test")
    # Should have exactly one handler
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)

    # Calling get_logger again should reuse the same handler (no duplicates)
    logger2 = get_logger("samy.test")
    assert logger is logger2
    assert len(logger2.handlers) == 1