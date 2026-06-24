from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.database.models import Base, TelemetryEventModel


class Database:
    """Simple SQLite-backed database for Samy.

    This wrapper initializes a SQLite engine and provides a session factory
    for repositories to use.
    """

    def __init__(self, url: str = "sqlite:///backend/database/sqlite.db") -> None:
        self.engine = create_engine(url, future=True)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def get_session(self) -> Session:
        """Create a new database session."""
        return self.SessionLocal()


class TelemetryRepository:
    """Repository for persisting and querying telemetry events."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def save_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Persist a telemetry event in the database."""
        session = self._db.get_session()
        try:
            event = TelemetryEventModel(event_type=event_type, payload=payload)
            session.add(event)
            session.commit()
        finally:
            session.close()

    def list_events(
        self,
        *,
        event_type: str | None = None,
        limit: int = 100,
    ) -> List[TelemetryEventModel]:
        """List recent telemetry events, optionally filtered by type."""
        session = self._db.get_session()
        try:
            query = session.query(TelemetryEventModel).order_by(TelemetryEventModel.id.desc())
            if event_type:
                query = query.filter(TelemetryEventModel.event_type == event_type)
            return query.limit(limit).all()
        finally:
            session.close()