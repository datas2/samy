from __future__ import annotations

from backend.rag.chunker import Chunk, simple_chunk_text


def test_simple_chunk_text_returns_empty_for_empty_text() -> None:
    chunks = simple_chunk_text("", source="test")
    assert chunks == []


def test_simple_chunk_text_produces_non_overlapping_last_chunk() -> None:
    text = "a" * 1000
    chunks = simple_chunk_text(text, source="file1", max_chars=400, overlap=100)
    # Expect 3 chunks: [0-400), [300-700), [600-1000)
    assert len(chunks) == 3
    assert chunks[0].offset == 0
    assert chunks[1].offset == 300
    assert chunks[2].offset == 600
    # Ensure content length respects max_chars
    assert len(chunks[0].content) <= 400
    assert len(chunks[1].content) <= 400
    assert len(chunks[2].content) <= 400