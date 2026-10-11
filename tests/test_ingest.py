"""
Basic unit tests for the ingestion pipeline. These test structure/logic
that doesn't require a live API call (chunking), plus a smoke test for
document loading.

Run with:
    pytest tests/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingest import chunk_documents, load_documents  # noqa: E402


def test_load_documents_returns_all_sample_files():
    docs = load_documents()
    assert len(docs) == 3, "Expected 3 sample markdown docs in the knowledge base"


def test_chunk_documents_produces_multiple_chunks():
    docs = load_documents()
    chunks = chunk_documents(docs, chunk_size=300, chunk_overlap=50)
    assert len(chunks) > len(docs), "Chunking should split docs into more, smaller pieces"


def test_chunks_respect_size_bound():
    docs = load_documents()
    chunks = chunk_documents(docs, chunk_size=300, chunk_overlap=50)
    # Allow some slack since splitting favors semantic boundaries
    oversized = [c for c in chunks if len(c.page_content) > 500]
    assert len(oversized) == 0, "No chunk should wildly exceed the configured chunk size"
