from __future__ import annotations

"""
Core constants for Samy.

This module centralizes environment variable names, default values and other
string constants used across the application.
"""

# Environment variable names
ENV_OLLAMA_BASE_URL = "OLLAMA_BASE_URL"
ENV_OLLAMA_MODEL = "OLLAMA_MODEL"

ENV_SAMY_LOG_LEVEL = "SAMY_LOG_LEVEL"
ENV_SAMY_ENV = "SAMY_ENV"  # e.g. "local", "dev", "prod"

# Default values
DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_MODEL = "qwen3.1:latest"

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_ENV = "local"