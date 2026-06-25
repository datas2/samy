from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from backend.rag import ingest as ingest_module


class DummyVectorStore:
    def __init__(self) -> None:
        self.added_chunks: List[Dict[str, Any]] = []

    def add_chunks(self, chunks) -> None:
        for c in chunks:
            self.added_chunks.append(
                {"content": c.content, "source": c.source, "offset": c.offset}
            )


def test_ingest_knowledge_directory_reads_files_and_adds_chunks(tmp_path, monkeypatch) -> None:
    # Create two sample files
    file1 = tmp_path / "doc1.md"
    file1.write_text("Hello world", encoding="utf-8")
    file2 = tmp_path / "doc2.txt"
    file2.write_text("Another document", encoding="utf-8")

    dummy_store = DummyVectorStore()

    class DummyVectorStoreFactory:
        def __init__(self, collection_name: str = "samy_knowledge") -> None:
            self.store = dummy_store

        def add_chunks(self, chunks) -> None:
            self.store.add_chunks(chunks)

    monkeypatch.setattr(ingest_module, "VectorStore", DummyVectorStoreFactory)

    ingest_module.ingest_knowledge_directory(root_dir=tmp_path, collection_name="test_collection")

    assert len(dummy_store.added_chunks) >= 2
    sources = {c["source"] for c in dummy_store.added_chunks}
    assert str(file1) in sources
    assert str(file2) in sources