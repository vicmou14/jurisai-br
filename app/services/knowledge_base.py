from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

@dataclass(frozen=True)
class LegalSource:
    id: str
    title: str
    content: str
    source: str
    topics: tuple[str, ...]

SOURCES = (
    LegalSource(
        id="cf88-art-5",
        title="Constituição Federal de 1988 — art. 5º",
        content="Todos são iguais perante a lei. São assegurados direitos fundamentais, devido processo legal, contraditório e ampla defesa nos termos constitucionais.",
        source="Base local demonstrativa; validar texto oficial e redação vigente.",
        topics=("constitucional", "direitos fundamentais", "defesa"),
    ),
    LegalSource(
        id="cdc-art-6",
        title="Código de Defesa do Consumidor — direitos básicos",
        content="O consumidor possui direitos básicos relacionados à informação, proteção contra práticas abusivas e reparação de danos, conforme a legislação aplicável.",
        source="Base local demonstrativa; validar texto oficial e redação vigente.",
        topics=("consumidor", "produto", "serviço", "cobrança"),
    ),
    LegalSource(
        id="clt-geral",
        title="Consolidação das Leis do Trabalho — relações de trabalho",
        content="Relações de emprego e trabalho são disciplinadas pela legislação trabalhista, contratos, jornada, remuneração e demais normas aplicáveis.",
        source="Base local demonstrativa; validar texto oficial e redação vigente.",
        topics=("trabalhista", "emprego", "salário", "demissão"),
    ),
    LegalSource(
        id="cc-contratos",
        title="Código Civil — contratos e responsabilidade civil",
        content="A legislação civil disciplina contratos, obrigações, responsabilidade civil e reparação de danos, observados os requisitos legais do caso concreto.",
        source="Base local demonstrativa; validar texto oficial e redação vigente.",
        topics=("civil", "contrato", "indenização", "dano"),
    ),
)

def _tokens(text: str) -> set[str]:
    return {token.lower().strip('.,;:!?()[]{}\"\'') for token in text.split() if token.strip()}

def retrieve(query: str, limit: int = 3) -> list[dict]:
    query_tokens = _tokens(query)
    scored = []
    for item in SOURCES:
        haystack = _tokens(item.title + " " + item.content + " " + " ".join(item.topics))
        score = len(query_tokens & haystack)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [
        {"id": item.id, "title": item.title, "content": item.content, "source": item.source, "score": score}
        for score, item in scored[:limit]
    ]
