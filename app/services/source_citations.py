from __future__ import annotations

from urllib.parse import urlparse


def normalize_source_url(value: str | None) -> str | None:
    if not value:
        return None
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return value.strip()


def citation_from_document(document) -> dict:
    return {
        "document_id": document.id,
        "title": document.title,
        "source": document.source,
        "category": document.category,
        "url": normalize_source_url(document.source),
    }


def has_grounded_sources(sources: list[dict]) -> bool:
    return any(item.get("source") for item in sources)
