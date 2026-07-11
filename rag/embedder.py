"""
rag/embedder.py
Initialises the sentence-transformer embedding function used by ChromaDB.
"""
from __future__ import annotations

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config.settings import get_settings

settings = get_settings()


def get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    """Return a ChromaDB-compatible sentence-transformer embedding function."""
    return SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model
    )
