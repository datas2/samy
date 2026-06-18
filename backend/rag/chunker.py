from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class Chunk:
    """Represent a single text chunk with optional metadata.

    Each chunk contains the raw text content and a source identifier, which can
    be used to trace back to the original document or file.
    """
    content: str
    source: str
    offset: int


def simple_chunk_text(
    text: str,
    *,
    source: str,
    max_chars: int = 800,
    overlap: int = 100,
) -> List[Chunk]:
    """Split a text into overlapping character-based chunks.

    This chunker is intentionally simple and focuses on robustness rather than
    linguistic awareness, making it suitable for docs, code and mixed content.

    Args:
        text: Input text to be chunked.
        source: Identifier of the source document (e.g., file path).
        max_chars: Maximum number of characters per chunk.
        overlap: Number of characters to overlap between consecutive chunks.

    Returns:
        List[Chunk]: List of chunk objects with content, source and offset.
    """
    chunks: List[Chunk] = []
    if not text:
        return chunks

    start = 0
    length = len(text)

    while start < length:
        end = min(start + max_chars, length)
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(Chunk(content=chunk_text, source=source, offset=start))
        if end == length:
            break
        start = max(0, end - overlap)

    return chunks