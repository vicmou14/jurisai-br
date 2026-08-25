from __future__ import annotations

from app.services.embedding_provider import get_provider


def index_text(text: str) -> dict:
    provider = get_provider()
    vector = provider.embed_one(text)
    return {"provider": provider.name, "dimensions": len(vector), "vector": vector}


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
