from app.services import text_generation


class DummyResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"models": [{"name": "qwen3:8b"}]}


def test_ollama_status_reports_available_model(monkeypatch):
    monkeypatch.setenv("JURISAI_TEXT_PROVIDER", "ollama")
    monkeypatch.setenv("JURISAI_OLLAMA_MODEL", "qwen3:8b")
    monkeypatch.setenv("JURISAI_OLLAMA_URL", "http://127.0.0.1:11434")
    monkeypatch.setattr(text_generation.httpx, "get", lambda *args, **kwargs: DummyResponse())

    status = text_generation.get_text_provider_status()

    assert status["provider"] == "ollama"
    assert status["reachable"] is True
    assert status["model_available"] is True


def test_ollama_status_reports_unreachable(monkeypatch):
    monkeypatch.setenv("JURISAI_TEXT_PROVIDER", "ollama")

    def fail(*args, **kwargs):
        raise text_generation.httpx.ConnectError("offline")

    monkeypatch.setattr(text_generation.httpx, "get", fail)
    status = text_generation.get_text_provider_status()

    assert status["reachable"] is False
    assert status["model_available"] is False
