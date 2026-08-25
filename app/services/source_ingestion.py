from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from app.services.legal_store import save_document


def normalize_document(source_name: str, source_url: str, title: str, content: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    digest = sha256(f"{source_url}|{title}|{content}".encode("utf-8")).hexdigest()
    return {
        "id": digest,
        "source_name": source_name,
        "source_url": source_url,
        "title": title.strip(),
        "content": content.strip(),
        "metadata": metadata or {},
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }


def ingest_document(source_name: str, source_url: str, title: str, content: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    document = normalize_document(source_name, source_url, title, content, metadata)
    if not document["content"]:
        raise ValueError("O conteúdo jurídico não pode ser vazio.")
    save_document(document)
    return document
