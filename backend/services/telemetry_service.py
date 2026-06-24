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

    Each event records a type, timestamp and arbitrary payload with metadata
    about the operation being executed.
    """
    event_type: str
    timestamp: datetime
    payload: Dict[str, Any]


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

    def record_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Record a telemetry event using the configured logger.

        Args:
            event_type: High-level type of the event (e.g., "explain", "review").
            payload: Arbitrary metadata associated with the event.
        """
        event = TelemetryEvent(
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            payload=payload,
        )

        # Log-based telemetry
        self._logger.info(
            "Telemetry event",
            extra={
                "event_type": event.event_type,
                "timestamp": event.timestamp.isoformat(),
                "payload": json.dumps(event.payload, ensure_ascii=False),
            },
        )

        # Optional persistence in database
        try:
            self._repository.save_event(event.event_type, event.payload)
        except Exception as exc:
            # Best-effort: do not break main flow if DB fails
            self._logger.error("Failed to persist telemetry event", extra={"error": str(exc)})