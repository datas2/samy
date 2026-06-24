from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def backup_sqlite_db(
    db_path: str | Path = "backend/database/sqlite.db",
    backup_dir: str | Path = "backups",
) -> Path:
    """Create a timestamped backup of the SQLite database.

    Args:
        db_path: Path to the main SQLite file.
        backup_dir: Directory where backups will be stored.

    Returns:
        Path: Path to the created backup file.
    """
    db_path = Path(db_path)
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"sqlite_{timestamp}.db"

    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found at {db_path}")

    import sqlite3
    with (
        sqlite3.connect(str(db_path)) as source_conn,
        sqlite3.connect(str(backup_path)) as backup_conn,
    ):
        source_conn.backup(backup_conn)
    return backup_path


if __name__ == "__main__":
    backup_file = backup_sqlite_db()
    print(f"Database backup created at: {backup_file}")