from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QualityAssessment:
    grounded: bool
    source_count: int
    reason: str


def assess_sources(sources: list[dict[str, Any]] | None) -> QualityAssessment:
    sources = sources or []
    if not sources:
        return QualityAssessment(False, 0, "Nenhuma fonte relevante foi recuperada.")
    return QualityAssessment(True, len(sources), "Resposta fundamentada em fontes recuperadas.")


def apply_quality_gate(result: dict[str, Any]) -> dict[str, Any]:
    assessment = assess_sources(result.get("sources"))
    return {
        **result,
        "grounded": assessment.grounded,
        "source_count": assessment.source_count,
        "quality_reason": assessment.reason,
    }
