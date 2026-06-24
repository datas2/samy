from __future__ import annotations

import contextlib
from pathlib import Path

from backend.rag.ingest import ingest_knowledge_directory


def build_embeddings_for_knowledge(
    knowledge_dir: str | Path = "knowledge",
    collection_name: str = "samy_knowledge",
) -> None:
    """Build embeddings for the local knowledge base.

    This script walks through the knowledge directory, chunks documents,
    generates embeddings via Ollama and stores them in the vector store.
    """
    import chromadb
    # Ensure the collection reflects the current repo state (no duplicates/stale docs).
    client = chromadb.Client()

    with contextlib.suppress(Exception):
        client.delete_collection(collection_name)
    
    ingest_knowledge_directory(root_dir=knowledge_dir, collection_name=collection_name)


if __name__ == "__main__":
    build_embeddings_for_knowledge()
    print("Embeddings built for knowledge directory.")