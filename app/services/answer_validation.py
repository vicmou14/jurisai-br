from __future__ import annotations

from typing import Any


def validate_legal_research(result: dict[str, Any]) -> dict[str, Any]:
    sources = result.get("sources") or []
    answer = str(result.get("answer") or "").strip()
    if not answer:
        result["answer"] = "Não foi possível produzir uma resposta com segurança."
    result["requires_human_review"] = not bool(result.get("grounded"))
    result["citation_check"] = bool(sources)
    return result
