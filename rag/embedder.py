"""
rag/embedder.py
Initialises the sentence-transformer embedding function used by ChromaDB.

NOTE: The project root contains a folder called ``datasets/`` which shadows
the HuggingFace ``datasets`` package that sentence-transformers depends on.
We work around this by temporarily removing the repo root from sys.path
before importing, then restoring it afterwards.
"""
from __future__ import annotations

import sys
from pathlib import Path

from config.settings import get_settings
from utils.logger import logger

# The repo root (parent of this file's parent) may shadow stdlib/site-packages
_REPO_ROOT = str(Path(__file__).resolve().parent.parent)


def get_embedding_function():
    """Return a ChromaDB-compatible sentence-transformer embedding function.

    ChromaDB's SentenceTransformerEmbeddingFunction expects the short model
    name (e.g. 'all-MiniLM-L6-v2'), not the full HuggingFace path
    ('sentence-transformers/all-MiniLM-L6-v2').

    Falls back to ChromaDB's default embedding function if sentence-transformers
    cannot be imported (e.g. the local ``datasets/`` folder shadows the package).
    """
    settings = get_settings()
    model_name = settings.embedding_model
    # Strip the "sentence-transformers/" org prefix if present
    if model_name.startswith("sentence-transformers/"):
        model_name = model_name.split("/", 1)[1]

    # Temporarily remove the repo root from sys.path so the local ``datasets/``
    # folder does not shadow the HuggingFace ``datasets`` package.
    _removed = _REPO_ROOT in sys.path
    if _removed:
        sys.path.remove(_REPO_ROOT)
    try:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
        fn = SentenceTransformerEmbeddingFunction(model_name=model_name)
        return fn
    except Exception as exc:
        logger.warning(
            f"SentenceTransformerEmbeddingFunction unavailable ({exc}). "
            "Falling back to ChromaDB default embedding function."
        )
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
        return DefaultEmbeddingFunction()
    finally:
        # Always restore sys.path
        if _removed and _REPO_ROOT not in sys.path:
            sys.path.insert(0, _REPO_ROOT)
