from __future__ import annotations

from app.services.knowledge_base import retrieve


def semantic_search(query: str, limit: int = 5) -> list[dict]:
    """Interface estável para busca jurídica.

    A implementação atual usa ranking lexical local. A camada pode ser trocada
    por embeddings e banco vetorial sem alterar os endpoints consumidores.
    """
    return retrieve(query, limit=limit)
