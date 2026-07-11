"""
rag/ingestor.py

Document ingestion pipeline.
Loads PDFs and text files from the docs/ directory, splits them into
chunks, embeds them, and stores them in ChromaDB.

Usage:
    python -m rag.ingestor
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import List, Tuple

from utils.logger import logger

# Supported file extensions
_SUPPORTED = {".pdf", ".txt", ".md", ".docx"}
_DOCS_DIR   = Path(__file__).parent.parent / "docs"
_CHUNK_SIZE = 512
_OVERLAP    = 64


def _chunk_text(text: str, chunk_size: int = _CHUNK_SIZE, overlap: int = _OVERLAP) -> List[str]:
    """Split *text* into overlapping chunks of roughly *chunk_size* characters."""
    chunks, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if len(c) > 50]   # discard tiny chunks


def _load_pdf(path: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _load_docx(path: Path) -> str:
    from docx import Document
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def _load_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return _load_pdf(path)
    if ext == ".docx":
        return _load_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def _doc_id(text: str, source: str, idx: int) -> str:
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    return f"{Path(source).stem}_{idx}_{h}"


def ingest(docs_dir: Path = _DOCS_DIR) -> int:
    """Ingest all supported documents from *docs_dir* into ChromaDB. Returns chunk count."""
    from rag.vector_store import VectorStore
    store = VectorStore()

    texts:     List[str]  = []
    metadatas: List[dict] = []
    ids:       List[str]  = []

    if not docs_dir.exists():
        logger.warning(f"Docs directory not found: {docs_dir}")
        return 0

    files = [f for f in docs_dir.rglob("*") if f.is_file() and f.suffix.lower() in _SUPPORTED]
    if not files:
        logger.warning("No supported documents found for ingestion.")
        return 0

    for fpath in files:
        logger.info(f"Ingesting: {fpath.name}")
        try:
            raw = _load_file(fpath)
            chunks = _chunk_text(raw)
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({"source": fpath.name, "path": str(fpath)})
                ids.append(_doc_id(chunk, fpath.name, i))
        except Exception as exc:
            logger.error(f"Failed to ingest {fpath.name}: {exc}")

    if texts:
        store.add_texts(texts, metadatas, ids)

    logger.info(f"Ingestion complete. Total chunks: {len(texts)}")
    return len(texts)


if __name__ == "__main__":
    ingest()
