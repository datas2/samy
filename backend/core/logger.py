from __future__ import annotations

import logging
import os
from typing import Optional

from backend.core import constants


def _get_log_level_from_env() -> int:
    """
    Resolve the log level based on SAMY_LOG_LEVEL or default.

    Returns:
        int: Logging level constant from the logging module.
    """
    level_str = os.getenv(constants.ENV_SAMY_LOG_LEVEL, constants.DEFAULT_LOG_LEVEL).upper()
    return getattr(logging, level_str, logging.INFO)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger for the Samy application.

    This logger uses a simple, structured format and respects the log level
    defined via environment variables, allowing different verbosity per
    environment without code changes.

    Args:
        name: Optional logger name. If None, the root "samy" logger is used.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger_name = name or "samy"
    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(_get_log_level_from_env())

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger