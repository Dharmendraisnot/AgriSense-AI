"""
agents/rag_agent.py

Knowledge Retrieval Agent.
Performs semantic search over the ChromaDB vector store and passes
retrieved context to IBM Granite for answer generation.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from utils.logger import logger


class RAGAgent(BaseAgent):
    """Answers general farming questions using RAG + IBM Granite."""

    async def run(
        self,
        message: str = "",
        location: Optional[str] = None,
        language: str = "en",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        query = message

        # ── Retrieve relevant chunks ───────────────────────────
        docs, sources = self._retrieve(query)
        context = "\n\n".join(d.page_content for d in docs) if docs else ""

        # ── Build RAG prompt ───────────────────────────────────
        loc_clause = f" The farmer is located in {location}." if location else ""
        prompt = (
            f"You are AgriSense AI, a trusted agricultural advisor.{loc_clause}\n\n"
            + (f"Relevant knowledge base information:\n{context}\n\n" if context else "")
            + f"Farmer's question: {query}\n\n"
            f"Provide a clear, practical, and accurate answer based on the above information. "
            f"If the knowledge base lacks relevant info, answer from your agricultural expertise.\n\n"
            f"Answer:"
        )
        answer = self.generate(prompt)

        return {
            "answer":     answer,
            "sources":    sources or ["IBM Granite Knowledge"],
            "confidence": 0.80 if docs else 0.60,
        }

    @staticmethod
    def _retrieve(query: str) -> tuple[List[Any], List[str]]:
        """Retrieve documents from ChromaDB. Returns (docs, source_names)."""
        try:
            from rag.retriever import Retriever
            retriever = Retriever()
            docs = retriever.retrieve(query, k=4)
            sources = list({d.metadata.get("source", "Knowledge Base") for d in docs})
            return docs, sources
        except Exception as exc:
            logger.debug(f"RAGAgent retrieval skipped: {exc}")
            return [], []
