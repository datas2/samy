from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TelemetryEventModel(Base):
    """ORM model for telemetry events recorded by Samy.

    Each row stores a high-level event type, timestamp and JSON payload with
    additional metadata about the operation.
    """

    __tablename__ = "telemetry_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(64), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    payload = Column(JSON, nullable=False)