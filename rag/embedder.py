"""
rag/embedder.py
Initialises the sentence-transformer embedding function used by ChromaDB.
"""
from __future__ import annotations

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config.settings import get_settings


def get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    """Return a ChromaDB-compatible sentence-transformer embedding function.

    ChromaDB's SentenceTransformerEmbeddingFunction expects the short model
    name (e.g. 'all-MiniLM-L6-v2'), not the full HuggingFace path
    ('sentence-transformers/all-MiniLM-L6-v2').
    """
    settings = get_settings()
    model_name = settings.embedding_model
    # Strip the "sentence-transformers/" org prefix if present
    if model_name.startswith("sentence-transformers/"):
        model_name = model_name.split("/", 1)[1]
    return SentenceTransformerEmbeddingFunction(model_name=model_name)
