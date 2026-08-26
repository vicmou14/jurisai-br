from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class WritingProfile:
    key: str
    name: str
    rules: list[str]


CODER_PROFILE = WritingProfile(
    key="coder",
    name="Estilo CODER",
    rules=[
        "Utilizar linguagem institucional, técnica e jurídica, com defesa objetiva dos interesses da CODER.",
        "Adotar a estrutura adequada ao órgão destinatário e à natureza administrativa, regulatória, societária ou processual do caso.",
        "Identificar expressamente a CODER e seus dados institucionais quando pertinentes ao tipo de documento.",
        "Organizar fatos e fundamentos em tópicos numerados, com desenvolvimento argumentativo e pedidos claros.",
        "Usar tom institucional firme, respeitoso e cooperativo, sem perder densidade argumentativa.",
        "Não inventar fatos, documentos, normas, datas, valores ou precedentes."
    ],
)

OFFICE_PROFILE = WritingProfile(
    key="office",
    name="Estilo do Escritório",
    rules=[
        "Utilizar redação jurídica técnica, precisa e individualizada ao caso concreto.",
        "Desenvolver a narrativa de forma cronológica e demonstrativa, conectando fatos, prova e consequência jurídica.",
        "Estruturar a peça conforme a natureza processual e o objetivo indicado na instrução do usuário.",
        "Priorizar fundamentação concreta e evitar alegações genéricas ou fórmulas vazias.",
        "Reconhecer pontos desfavoráveis quando existirem e enfrentá-los tecnicamente.",
        "Não inventar fatos, documentos, normas, datas, valores ou precedentes."
    ],
)

PROFILES = {CODER_PROFILE.key: CODER_PROFILE, OFFICE_PROFILE.key: OFFICE_PROFILE}

CODER_PATTERN = re.compile(r"\b(CODER|COMPANHIA DE DESENVOLVIMENTO DE RONDONÓPOLIS)\b", re.IGNORECASE)


def select_profile(instruction: str, context: str | None = None) -> WritingProfile:
    combined = f"{instruction}\n{context or ''}"
    return CODER_PROFILE if CODER_PATTERN.search(combined) else OFFICE_PROFILE


def detect_document_type(instruction: str) -> str:
    normalized = instruction.lower()
    candidates = [
        ("petição inicial", "peticao_inicial"),
        ("contestação", "contestacao"),
        ("contestaçao", "contestacao"),
        ("manifestação", "manifestacao"),
        ("réplica", "replica"),
        ("recurso", "recurso"),
        ("ofício", "oficio"),
        ("parecer", "parecer"),
        ("habeas corpus", "habeas_corpus"),
        ("petição", "peticao"),
    ]
    for phrase, key in candidates:
        if phrase in normalized:
            return key
    return "documento_juridico"


def build_writing_brief(instruction: str, context: str | None = None) -> dict:
    profile = select_profile(instruction, context)
    return {
        "profile": profile.key,
        "profile_name": profile.name,
        "document_type": detect_document_type(instruction),
        "rules": profile.rules,
        "instruction": instruction.strip(),
        "context": (context or "").strip(),
        "supported_uploads": ["PDF", "DOCX"],
    }
