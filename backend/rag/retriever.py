from __future__ import annotations

from typing import List, Dict, Any

from backend.rag.vector_store import VectorStore


class KnowledgeRetriever:
    """High-level interface to retrieve knowledge snippets for Samy.

    The retriever wraps the vector store and provides a simple method to
    obtain relevant chunks given a user query, which can then be integrated
    into LLM prompts for RAG.
    """

    def __init__(
        self,
        collection_name: str = "samy_knowledge",
    ) -> None:
        self._store = VectorStore(collection_name=collection_name)

    def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Retrieve top-k knowledge chunks similar to the given query.

        Args:
            query: Input text describing the information need.
            k: Maximum number of results to return.

        Returns:
            List[Dict[str, Any]]: Retrieved chunks with content and metadata.
        """
        return self._store.query(query_text=query, k=k)