from __future__ import annotations

import os

import httpx
from openai import OpenAI

from app.services.draft_generation import build_draft_request

DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_MODEL = "qwen3:8b"
DEFAULT_OPENAI_MODEL = "gpt-5.6-sol"


def _build_prompt(draft: dict, instruction: str, context: str | None) -> str:
    return "\n".join([
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


def _generate_with_ollama(prompt: str) -> tuple[str, str]:
    base_url = os.getenv("JURISAI_OLLAMA_URL", "http://host.docker.internal:11434").rstrip("/")
    model = os.getenv("JURISAI_OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    try:
        response = httpx.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=float(os.getenv("JURISAI_TEXT_TIMEOUT", "300")),
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Não foi possível conectar ao Ollama. Instale o Ollama, execute o modelo configurado e mantenha o serviço ativo."
        ) from exc
    payload = response.json()
    text = str(payload.get("response") or "").strip()
    if not text:
        raise RuntimeError("O modelo local não retornou texto para a peça.")
    return text, model


def _generate_with_openai(prompt: str) -> tuple[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não configurada para o provedor openai.")
    model = os.getenv("JURISAI_OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    client = OpenAI(api_key=api_key)
    response = client.responses.create(model=model, input=prompt)
    text = (response.output_text or "").strip()
    if not text:
        raise RuntimeError("O modelo OpenAI não retornou texto para a peça.")
    return text, model


def generate_legal_draft(instruction: str, context: str | None = None, documents: list[dict] | None = None) -> dict:
    draft = build_draft_request(instruction, context, documents)
    prompt = _build_prompt(draft, instruction, context)
    provider = os.getenv("JURISAI_TEXT_PROVIDER", DEFAULT_PROVIDER).strip().lower()

    if provider == "ollama":
        text, model = _generate_with_ollama(prompt)
    elif provider == "openai":
        text, model = _generate_with_openai(prompt)
    else:
        raise RuntimeError("JURISAI_TEXT_PROVIDER inválido. Use 'ollama' ou 'openai'.")

    return {
        "title": draft["document_type"].replace("_", " ").title(),
        "content": text,
        "profile": draft["profile"],
        "profile_name": draft["profile_name"],
        "document_type": draft["document_type"],
        "provider": provider,
        "model": model,
        "documents_count": draft["documents_count"],
    }
