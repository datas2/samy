from __future__ import annotations

import shutil
from pathlib import Path


def import_playbooks(
    source_dir: str | Path,
    target_dir: str | Path = "knowledge/playbooks",
) -> None:
    """Import playbooks into the Samy knowledge base.

    Args:
        source_dir: Directory containing playbook files to be imported.
        target_dir: Destination directory under the knowledge base.
    """
    source = Path(source_dir)
    target = Path(target_dir)

    if not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")

    target.mkdir(parents=True, exist_ok=True)

    for path in source.rglob("*"):
        if path.is_file():
            rel = path.relative_to(source)
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scripts/import_playbooks.py <source_dir>")
        raise SystemExit(1)

    import_playbooks(sys.argv[1])
    print("Playbooks imported into knowledge base.")