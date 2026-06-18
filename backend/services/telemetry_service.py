from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from backend.core.logger import get_logger


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
    key events such as explain, review and optimize calls without requiring
    external infrastructure.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger or get_logger("samy.telemetry")

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
        self._logger.info(
            "Telemetry event",
            extra={
                "event_type": event.event_type,
                "timestamp": event.timestamp.isoformat(),
                "payload": json.dumps(event.payload, ensure_ascii=False),
            },
        )