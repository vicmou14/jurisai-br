from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LegalDocument
from app.services.embedding_provider import get_provider


def document_id(title: str, content: str, source: str) -> str:
    raw = f"{title}\n{content}\n{source}".encode("utf-8")
    return sha256(raw).hexdigest()


def _apply_embedding(document: LegalDocument) -> None:
    provider = get_provider()
    vector = provider.embed_one(f"{document.title}\n{document.content}")
    document.embedding = vector
    document.embedding_provider = provider.name
    document.embedding_dimensions = len(vector)
    document.embedded_at = datetime.now(timezone.utc)


def save_document(session: Session, title: str, content: str, source: str, category: str = "geral") -> LegalDocument:
    identifier = document_id(title, content, source)
    existing = session.get(LegalDocument, identifier)
    if existing:
        return existing
    document = LegalDocument(id=identifier, title=title, content=content, source=source, category=category)
    _apply_embedding(document)
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


def search_documents(session: Session, query: str, limit: int = 10) -> list[LegalDocument]:
    statement = select(LegalDocument).where(
        (LegalDocument.title.ilike(f"%{query}%")) | (LegalDocument.content.ilike(f"%{query}%"))
    ).limit(limit)
    return list(session.scalars(statement))
