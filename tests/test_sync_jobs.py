from app.services.sync_jobs import build_registry


def test_registry_contains_official_sources():
    registry = build_registry()
    assert registry.names() == ["planalto", "stf", "stj"]


def test_sources_without_configuration_are_safe(monkeypatch):
    monkeypatch.delenv("JURISAI_PLANALTO_URLS", raising=False)
    monkeypatch.delenv("JURISAI_STF_CSV", raising=False)
    registry = build_registry()
    assert registry.execute("planalto").imported == 0
    assert registry.execute("stf").imported == 0
