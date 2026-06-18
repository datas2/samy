from __future__ import annotations

from typing import Any, Dict, List

from backend.rag import retriever as retriever_module


class DummyVectorStore:
    def __init__(self) -> None:
        self.last_query: Dict[str, Any] | None = None

    def query(self, *, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        self.last_query = {"query_text": query_text, "k": k}
        return [
            {"content": "doc1", "source": "file1", "offset": 0},
            {"content": "doc2", "source": "file2", "offset": 10},
        ]


def test_knowledge_retriever_uses_vector_store(monkeypatch) -> None:
    captured_store: DummyVectorStore | None = None

    def fake_init(self, collection_name: str = "samy_knowledge") -> None:
        nonlocal captured_store
        captured_store = DummyVectorStore()
        # Replace internal _store with dummy
        self._store = captured_store  # type: ignore[attr-defined]

    monkeypatch.setattr(
        retriever_module.KnowledgeRetriever,
        "__init__",
        fake_init,
    )

    retriever = retriever_module.KnowledgeRetriever(collection_name="test_collection")
    results = retriever.retrieve("test query", k=2)

    assert captured_store is not None
    assert captured_store.last_query == {"query_text": "test query", "k": 2}
    assert len(results) == 2
    assert results[0]["content"] == "doc1"