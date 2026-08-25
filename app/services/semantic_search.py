from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LegalDocument
from app.services.embeddings import cosine_similarity, embed


def search(session: Session, query: str, limit: int = 5) -> list[dict]:
    query_vector = embed(query)
    documents = list(session.scalars(select(LegalDocument)))
    ranked = []
    for document in documents:
        score = cosine_similarity(query_vector, embed(f"{document.title} {document.content}"))
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
        }
        for score, document in ranked[:limit]
    ]
