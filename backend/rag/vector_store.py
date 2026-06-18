from __future__ import annotations

from typing import Any, Dict, List

import chromadb
from chromadb.api import ClientAPI

from backend.llm.embeddings import embed_text
from backend.rag.chunker import Chunk


class VectorStore:
    """Wrapper around ChromaDB for storing and querying text chunks.

    This class encapsulates a single Chroma collection and exposes methods
    for inserting chunked documents and performing similarity search.
    """

    def __init__(
        self,
        collection_name: str = "samy_knowledge",
        client: ClientAPI | None = None,
    ) -> None:
        self._client = client or chromadb.Client()
        self._collection = self._client.get_or_create_collection(collection_name)

    def add_chunks(self, chunks: List[Chunk]) -> None:
        """Add a list of chunks to the vector store.

        Args:
            chunks: List of Chunk objects to be indexed.
        """
        if not chunks:
            return

        texts = [c.content for c in chunks]
        ids = [f"{c.source}:{c.offset}" for c in chunks]
        metadatas: List[Dict[str, Any]] = [
            {"source": c.source, "offset": c.offset} for c in chunks
        ]

        embeddings = [embed_text(text) for text in texts]

        self._collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(
        self,
        query_text: str,
        *,
        k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Query the vector store for the most similar chunks to a given text.

        Args:
            query_text: Text used as the query for similarity search.
            k: Maximum number of results to return.

        Returns:
            List[Dict[str, Any]]: Results with content and metadata.
        """
        query_embedding = embed_text(query_text)

        result = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )

        hits: List[Dict[str, Any]] = []
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        hits.extend(
            {
                "content": doc,
                "source": meta.get("source"),
                "offset": meta.get("offset"),
            }
            for doc, meta in zip(documents, metadatas)
        )
        return hits