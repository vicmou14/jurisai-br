from sqlalchemy.orm import Session

from app.connectors.base import ExternalLegalDocument
from app.services.document_repository import save_document


def ingest_external(session: Session, document: ExternalLegalDocument) -> dict:
    saved = save_document(
        session,
        title=document.title,
        content=document.content,
        source=document.source,
        category=document.category,
    )
    return {"id": saved.id, "title": saved.title, "source": saved.source}
