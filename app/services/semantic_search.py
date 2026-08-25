from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LegalDocument
from app.services.embedding_provider import get_provider
from app.services.vector_index import cosine


def search(session: Session, query: str, limit: int = 5) -> list[dict]:
    provider = get_provider()
    query_vector = provider.embed_one(query)
    documents = list(session.scalars(select(LegalDocument)))
    ranked = []
    for document in documents:
        if not document.embedding or len(document.embedding) != len(query_vector):
            continue
        score = cosine(query_vector, document.embedding)
        if score > 0:
            ranked.append((score, document))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "source": document.source,
            "category": document.category,
            "score": round(score, 4),
            "embedding_provider": document.embedding_provider,
        }
        for score, document in ranked[:limit]
    ]
