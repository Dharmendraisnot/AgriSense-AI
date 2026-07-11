"""
rag/vector_store.py

ChromaDB vector store wrapper.
Provides initialise, add_documents, and query operations.

Compatible with chromadb >= 1.0.0 (pre-built wheels, no C++ compiler required).
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import chromadb

from config.settings import get_settings
from rag.embedder import get_embedding_function
from utils.logger import logger

app_settings = get_settings()


class VectorStore:
    """Thin wrapper around a persistent ChromaDB collection."""

    def __init__(self) -> None:
        persist_dir = Path(app_settings.chroma_persist_directory)
        persist_dir.mkdir(parents=True, exist_ok=True)

        # chromadb 1.x: Settings moved; anonymized_telemetry set via env var
        # ANONYMIZED_TELEMETRY=False or simply omit (default is False in 1.x)
        self._client = chromadb.PersistentClient(path=str(persist_dir))
        self._embedding_fn = get_embedding_function()
        self._collection = self._client.get_or_create_collection(
            name=app_settings.chroma_collection_name,
            embedding_function=self._embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            f"VectorStore ready – collection '{app_settings.chroma_collection_name}' "
            f"has {self._collection.count()} documents."
        )

    def add_texts(self, texts: List[str], metadatas: List[dict], ids: List[str]) -> None:
        """Add raw text chunks to the collection."""
        self._collection.upsert(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info(f"Added {len(texts)} chunks to vector store.")

    def query(self, query_text: str, n_results: int = 4) -> dict:
        """Perform a similarity search and return raw ChromaDB results."""
        return self._collection.query(
            query_texts=[query_text],
            n_results=min(n_results, max(1, self._collection.count())),
            include=["documents", "metadatas", "distances"],
        )

    def count(self) -> int:
        return self._collection.count()
