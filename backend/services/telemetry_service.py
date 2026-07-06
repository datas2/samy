from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from backend.core.logger import get_logger
from backend.database.repositories import Database, TelemetryRepository


@dataclass
class TelemetryEvent:
    """Represent a telemetry event captured by Samy.

    Each event records:
        - schema_version: version of the event schema (e.g., "v1")
        - event_type: type of the event (e.g., "sql_explain", "python_review")
        - timestamp: UTC timestamp
        - payload: arbitrary metadata
        - log_level: severity level ("INFO", "WARNING", "ERROR", etc.)
    """
    schema_version: str
    event_type: str
    timestamp: datetime
    payload: Dict[str, Any]
    log_level: str = "INFO"


class TelemetryService:
    """Simple telemetry service for logging Samy operations.

    This service focuses on lightweight logging-based telemetry, capturing
    key events such as explain, review and optimize calls, and can optionally
    persist them to a SQLite database.
    """

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        repository: Optional[TelemetryRepository] = None,
    ) -> None:
        self._logger = logger or get_logger("samy.telemetry")
        # Initialize database/repository only if provided to keep it optional
        self._repository = repository or TelemetryRepository(Database())

    @staticmethod
    def estimate_tokens_from_text(text: str) -> int:
        """Estimate the number of tokens from a text.

        This uses a simple heuristic based on whitespace-separated words,
        which is not model-accurate but provides a useful approximation of
        prompt size and costs across requests.
        """
        return len(text.split()) if text else 0

    def record_event(self, event_type: str, payload: Dict[str, Any], log_level: str = "INFO") -> None:
        """Record a telemetry event using the configured logger.

        Args:
            event_type: High-level type of the event (e.g., "sql_explain", "python_review").
            payload: Arbitrary metadata associated with the event.
            log_level: Severity level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
        """
        event = TelemetryEvent(
            schema_version="v1",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            payload=payload,
            log_level=log_level.upper(),
        )

        # Log-based telemetry
        extra = {
            "schema_version": event.schema_version,
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            "payload": json.dumps(event.payload, ensure_ascii=False),
        }

        if event.log_level == "DEBUG":
            self._logger.debug("Telemetry event", extra=extra)
        elif event.log_level == "INFO":
            self._logger.info("Telemetry event", extra=extra)
        elif event.log_level == "WARNING":
            self._logger.warning("Telemetry event", extra=extra)
        elif event.log_level == "ERROR":
            self._logger.error("Telemetry event", extra=extra)
        elif event.log_level == "CRITICAL":
            self._logger.critical("Telemetry event", extra=extra)
        else:
            self._logger.info("Telemetry event", extra=extra)

        # Optional persistence in database
        try:
            self._repository.save_event(event.event_type, event.payload)
        except Exception as exc:
            # Best-effort: do not break main flow if DB fails
            self._logger.error("Failed to persist telemetry event", extra={"error": str(exc)})