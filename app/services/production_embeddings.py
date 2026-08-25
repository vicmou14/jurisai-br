from __future__ import annotations

import os
from typing import Protocol

class EmbeddingProvider(Protocol):
    name: str
    dimensions: int
    def embed(self, texts: list[str]) -> list[list[float]]: ...

class DisabledEmbeddingProvider:
    name = "disabled"
    dimensions = 0
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise RuntimeError("Configure JURISAI_EMBEDDING_PROVIDER para habilitar embeddings de produção.")

def get_embedding_provider() -> EmbeddingProvider:
    provider = os.getenv("JURISAI_EMBEDDING_PROVIDER", "disabled").lower()
    if provider == "disabled":
        return DisabledEmbeddingProvider()
    raise RuntimeError(f"Provider não implementado: {provider}")
