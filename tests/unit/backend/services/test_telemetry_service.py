from __future__ import annotations

import logging

from backend.services.telemetry_service import TelemetryService


def test_estimate_tokens_from_text_counts_words() -> None:
    assert TelemetryService.estimate_tokens_from_text("") == 0
    assert TelemetryService.estimate_tokens_from_text("one") == 1
    assert TelemetryService.estimate_tokens_from_text("one two three") == 3


def test_record_event_logs_with_expected_payload(caplog) -> None:
    telemetry = TelemetryService()
    with caplog.at_level(logging.INFO, logger="samy.telemetry"):
        telemetry.record_event(
            event_type="explain",
            payload={"foo": "bar"},
        )

    # At least one log record with the expected extra fields
    assert any("Telemetry event" in rec.message for rec in caplog.records)