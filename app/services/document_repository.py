from __future__ import annotations

from hashlib import sha256
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LegalDocument


def document_id(title: str, content: str, source: str) -> str:
    raw = f"{title}\n{content}\n{source}".encode("utf-8")
    return sha256(raw).hexdigest()


def save_document(session: Session, title: str, content: str, source: str, category: str = "geral") -> LegalDocument:
    identifier = document_id(title, content, source)
    existing = session.get(LegalDocument, identifier)
    if existing:
        return existing
    document = LegalDocument(id=identifier, title=title, content=content, source=source, category=category)
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


def search_documents(session: Session, query: str, limit: int = 10) -> list[LegalDocument]:
    statement = select(LegalDocument).where(
        (LegalDocument.title.ilike(f"%{query}%")) | (LegalDocument.content.ilike(f"%{query}%"))
    ).limit(limit)
    return list(session.scalars(statement))
