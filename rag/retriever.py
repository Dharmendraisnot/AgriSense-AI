"""
rag/retriever.py

High-level retriever used by all agents.
Returns LangChain-compatible Document objects from ChromaDB similarity search.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from rag.vector_store import VectorStore
from utils.logger import logger


@dataclass
class Document:
    """Minimal LangChain-compatible document container."""
    page_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class Retriever:
    """Retrieves top-k relevant document chunks from ChromaDB."""

    def __init__(self) -> None:
        self._store = VectorStore()

    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """
        Retrieve *k* most-relevant document chunks for *query*.
        Returns an empty list if the store is empty.
        """
        if self._store.count() == 0:
            logger.debug("VectorStore is empty – skipping retrieval.")
            return []

        results = self._store.query(query, n_results=k)
        docs = []
        for text, meta in zip(
            results["documents"][0],
            results["metadatas"][0],
        ):
            docs.append(Document(page_content=text, metadata=meta or {}))

        logger.debug(f"Retrieved {len(docs)} chunks for query: {query[:60]}")
        return docs
