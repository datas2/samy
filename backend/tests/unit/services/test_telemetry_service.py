from __future__ import annotations

import logging

from backend.services.telemetry_service import TelemetryService


class DummyRepository:
    """Simple dummy repository to avoid real DB writes in unit tests."""
    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def save_event(self, event_type: str, payload: dict) -> None:
        self.events.append((event_type, payload))


def test_estimate_tokens_from_text_counts_words() -> None:
    assert TelemetryService.estimate_tokens_from_text("") == 0
    assert TelemetryService.estimate_tokens_from_text("one") == 1
    assert TelemetryService.estimate_tokens_from_text("one two three") == 3


def test_record_event_logs_with_expected_payload(caplog) -> None:
    # Use DummyRepository to avoid touching real SQLite
    repo = DummyRepository()
    telemetry = TelemetryService(repository=repo)

    with caplog.at_level(logging.INFO, logger="samy.telemetry"):
        telemetry.record_event(
            event_type="explain",
            payload={"foo": "bar"},
            log_level="INFO",
        )

    # At least one log record with the expected message
    assert any("Telemetry event" in rec.message for rec in caplog.records)

    # Repository should have received the event
    assert repo.events == [("explain", {"foo": "bar"})]


def test_record_event_uses_error_log_level(caplog) -> None:
    repo = DummyRepository()
    telemetry = TelemetryService(repository=repo)

    with caplog.at_level(logging.ERROR, logger="samy.telemetry"):
        telemetry.record_event(
            event_type="explain_error",
            payload={"foo": "bar"},
            log_level="ERROR",
        )

    # Ensure an ERROR-level telemetry log was emitted
    assert any(
        "Telemetry event" in rec.message and rec.levelno == logging.ERROR
        for rec in caplog.records
    )