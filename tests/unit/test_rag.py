"""
tests/unit/test_rag.py
Unit tests for the RAG pipeline.
"""
from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest


class TestVectorStore:
    @patch("rag.embedder.SentenceTransformerEmbeddingFunction")
    @patch("rag.vector_store.chromadb.PersistentClient")
    def test_vector_store_init(self, mock_client, mock_stef):
        """VectorStore should initialise without error (chromadb 1.x compatible)."""
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        mock_stef.return_value = MagicMock()   # skip actual sentence-transformer model load

        from rag.vector_store import VectorStore
        store = VectorStore()
        assert store.count() == 0


class TestIngestor:
    def test_chunk_text_basic(self):
        from rag.ingestor import _chunk_text
        text = "word " * 300          # ~1500 chars
        chunks = _chunk_text(text, chunk_size=512, overlap=64)
        assert len(chunks) > 1
        for c in chunks:
            assert len(c) > 50

    def test_chunk_text_short(self):
        from rag.ingestor import _chunk_text
        text = "Short."
        chunks = _chunk_text(text, chunk_size=512, overlap=64)
        # Too short – should be filtered
        assert chunks == []
