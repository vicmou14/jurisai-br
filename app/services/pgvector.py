from __future__ import annotations

import math
from collections import Counter
from app.services.embeddings import embed


def dense_embedding(text: str, dimensions: int = 256) -> list[float]:
    """Deterministic hashed embedding fallback, replaceable by a real provider."""
    vector = [0.0] * dimensions
    counts: Counter[str] = embed(text)
    for token, count in counts.items():
        index = hash(token) % dimensions
        vector[index] += float(count)
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def vector_literal(vector: list[float]) -> str:
    return "[" + ",".join(f"{value:.8f}" for value in vector) + "]"
