from __future__ import annotations

import os
from typing import Protocol
from app.services.pgvector import dense_embedding

class Provider(Protocol):
    name: str
    dimensions: int
    def embed_one(self, text: str) -> list[float]: ...

class LocalProvider:
    name = "local-hash"
    dimensions = 256
    def embed_one(self, text: str) -> list[float]:
        return dense_embedding(text, self.dimensions)

def get_provider() -> Provider:
    provider = os.getenv("JURISAI_EMBEDDING_PROVIDER", "local").lower()
    if provider in {"local", "local-hash"}:
        return LocalProvider()
    raise RuntimeError(f"Embedding provider não configurado: {provider}")
