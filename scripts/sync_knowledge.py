from __future__ import annotations

from pathlib import Path

from backend.rag.ingest import ingest_knowledge_directory


def sync_knowledge(
    knowledge_dir: str | Path = "knowledge",
    collection_name: str = "samy_knowledge",
) -> None:
    """Synchronize the knowledge directory with the vector store.

    This script re-ingests all knowledge files so that the vector store
    reflects the current state of the repository.
    """
    ingest_knowledge_directory(root_dir=knowledge_dir, collection_name=collection_name)


if __name__ == "__main__":
    sync_knowledge()
    print("Knowledge base synchronized with vector store.")