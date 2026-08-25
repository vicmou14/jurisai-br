from __future__ import annotations

import json
import os
from typing import Any

from app.services.embeddings import cosine_similarity, embed

VECTOR_MODE = os.getenv("JURISAI_VECTOR_MODE", "local")


def build_vector(text: str) -> dict[str, int]:
    return dict(embed(text))


def score(query: str, document: str) -> float:
    return cosine_similarity(embed(query), embed(document))


def serialize(vector: dict[str, int]) -> str:
    return json.dumps(vector, ensure_ascii=False, sort_keys=True)


def deserialize(value: str) -> dict[str, int]:
    return json.loads(value)


def backend_info() -> dict[str, Any]:
    return {
        "mode": VECTOR_MODE,
        "embedding": "token-frequency-baseline",
        "pgvector_ready": True,
        "note": "Configure a production embedding provider and pgvector index before large-scale deployment.",
    }
