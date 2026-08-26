from __future__ import annotations

import os

from openai import OpenAI

from app.services.draft_generation import build_draft_request

DEFAULT_MODEL = "gpt-5.6-sol"


def generate_legal_draft(instruction: str, context: str | None = None, documents: list[dict] | None = None) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    draft = build_draft_request(instruction, context, documents)
    model = os.getenv("JURISAI_TEXT_MODEL", DEFAULT_MODEL)
    prompt = "\n".join([
        "Você é o gerador de texto jurídico do JurisAI-BR.",
        "Produza somente o texto integral da peça solicitada, sem comentários sobre o processo de geração.",
        f"Perfil de redação: {draft['profile_name']}.",
        f"Tipo de peça: {draft['document_type'].replace('_', ' ')}.",
        "Regras obrigatórias:",
        *[f"- {rule}" for rule in draft["generation_instructions"]],
        "Estrutura recomendada:",
        *[f"- {section}" for section in draft["sections"]],
        f"Instrução do usuário:\n{instruction}",
        f"Contexto adicional:\n{context or '[não fornecido]'}",
        f"Documentos disponíveis:\n{draft['documents_context'] or '[nenhum documento]'}",
    ])

    client = OpenAI(api_key=api_key)
    response = client.responses.create(model=model, input=prompt)
    text = (response.output_text or "").strip()
    if not text:
        raise RuntimeError("O modelo não retornou texto para a peça.")

    return {
        "title": draft["document_type"].replace("_", " ").title(),
        "content": text,
        "profile": draft["profile"],
        "profile_name": draft["profile_name"],
        "document_type": draft["document_type"],
        "model": model,
        "documents_count": draft["documents_count"],
    }
