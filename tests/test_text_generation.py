import pytest

from app.services import text_generation


def test_ollama_provider_returns_generated_text(monkeypatch):
    monkeypatch.setenv("JURISAI_TEXT_PROVIDER", "ollama")
    monkeypatch.setenv("JURISAI_OLLAMA_MODEL", "qwen3:8b")

    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"response": "TEXTO JURÍDICO GERADO"}

    monkeypatch.setattr(text_generation.httpx, "post", lambda *args, **kwargs: Response())
    result = text_generation.generate_legal_draft("Faça uma manifestação.")
    assert result["provider"] == "ollama"
    assert result["model"] == "qwen3:8b"
    assert result["content"] == "TEXTO JURÍDICO GERADO"


def test_invalid_provider_is_rejected(monkeypatch):
    monkeypatch.setenv("JURISAI_TEXT_PROVIDER", "invalido")
    with pytest.raises(RuntimeError, match="JURISAI_TEXT_PROVIDER inválido"):
        text_generation.generate_legal_draft("Faça uma manifestação.")


def test_openai_provider_requires_key(monkeypatch):
    monkeypatch.setenv("JURISAI_TEXT_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY não configurada"):
        text_generation.generate_legal_draft("Faça uma manifestação.")
