from __future__ import annotations

import re
from typing import Any

from app.services.legal_store import load_documents

STOPWORDS = {"a", "o", "e", "de", "do", "da", "dos", "das", "em", "para", "por", "com", "um", "uma", "que", "sobre"}


def tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[\wÀ-ÿ]+", text.lower()) if token not in STOPWORDS}


def search_documents(query: str, limit: int = 5) -> list[dict[str, Any]]:
    query_tokens = tokens(query)
    scored: list[tuple[int, dict[str, Any]]] = []
    for document in load_documents():
        haystack = tokens(document.get("title", "") + " " + document.get("content", ""))
        score = len(query_tokens & haystack)
        if score:
            result = dict(document)
            result["score"] = score
            scored.append((score, result))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [item for _, item in scored[:limit]]
