from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from backend.rag.chunker import Chunk, simple_chunk_text
from backend.rag.vector_store import VectorStore


def _iter_text_files(root: Path) -> Iterable[Path]:
    """Yield all text-like files from a root directory.

    Currently this considers `.md`, `.txt` and `.rst` files as text sources.
    """
    for path in root.rglob("*"):
        if path.suffix.lower() in {".md", ".txt", ".rst"} and path.is_file():
            yield path


def ingest_knowledge_directory(
    root_dir: str | Path,
    *,
    collection_name: str = "samy_knowledge",
) -> None:
    """Ingest knowledge files into the vector store.

    This function walks through the given directory, chunks each text file and
    indexes the chunks into the configured vector store.

    Args:
        root_dir: Directory containing knowledge base files.
        collection_name: Name of the Chroma collection to use.
    """
    root = Path(root_dir)
    store = VectorStore(collection_name=collection_name)

    for file_path in _iter_text_files(root):
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        chunks: List[Chunk] = simple_chunk_text(
            text,
            source=str(file_path),
            max_chars=800,
            overlap=100,
        )
        store.add_chunks(chunks)