from __future__ import annotations

from typing import Any, Dict, List

from backend.rag.chunker import Chunk
from backend.rag import vector_store as vector_store_module


class DummyCollection:
    def __init__(self) -> None:
        self.add_calls: Dict[str, Any] | None = None
        self.query_calls: Dict[str, Any] | None = None

    def add(self, *, ids, documents, metadatas, embeddings) -> None:  # type: ignore[override]
        self.add_calls = {
            "ids": ids,
            "documents": documents,
            "metadatas": metadatas,
            "embeddings": embeddings,
        }

    def query(self, *, query_embeddings, n_results):  # type: ignore[override]
        self.query_calls = {
            "query_embeddings": query_embeddings,
            "n_results": n_results,
        }
        return {
            "documents": [["doc1", "doc2"]],
            "metadatas": [[{"source": "file1", "offset": 0}, {"source": "file2", "offset": 10}]],
        }


class DummyClient:
    def __init__(self) -> None:
        self.collection = DummyCollection()

    def get_or_create_collection(self, name: str) -> DummyCollection:
        return self.collection


def test_vector_store_add_chunks_uses_embeddings(monkeypatch) -> None:
    # Monkeypatch chromadb.Client and embed_text
    monkeypatch.setattr(vector_store_module.chromadb, "Client", lambda: DummyClient())
    monkeypatch.setattr(vector_store_module, "embed_text", lambda text: [0.1, 0.2])

    vs = vector_store_module.VectorStore(collection_name="test_collection")

    chunks = [
        Chunk(content="chunk1", source="file1", offset=0),
        Chunk(content="chunk2", source="file2", offset=10),
    ]
    vs.add_chunks(chunks)

    collection = vs._collection  # type: ignore[attr-defined]
    assert collection.add_calls is not None
    assert collection.add_calls["ids"] == ["file1:0", "file2:10"]
    assert collection.add_calls["documents"] == ["chunk1", "chunk2"]
    assert collection.add_calls["metadatas"] == [
        {"source": "file1", "offset": 0},
        {"source": "file2", "offset": 10},
    ]
    # embed_text mocked to return [0.1, 0.2] for each document
    assert collection.add_calls["embeddings"] == [[0.1, 0.2], [0.1, 0.2]]


def test_vector_store_query_returns_hits(monkeypatch) -> None:
    dummy_client = DummyClient()
    monkeypatch.setattr(vector_store_module.chromadb, "Client", lambda: dummy_client)
    monkeypatch.setattr(vector_store_module, "embed_text", lambda text: [0.5, 0.6])

    vs = vector_store_module.VectorStore(collection_name="test_collection")
    hits = vs.query("hello", k=2)

    collection = vs._collection  # type: ignore[attr-defined]
    assert collection.query_calls is not None
    assert collection.query_calls["n_results"] == 2
    assert hits == [
        {"content": "doc1", "source": "file1", "offset": 0},
        {"content": "doc2", "source": "file2", "offset": 10},
    ]