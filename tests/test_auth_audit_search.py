from app.services.audit import log_event
from app.services.search import semantic_search


def test_search_returns_results():
    results = semantic_search("produto defeituoso consumidor")
    assert results


def test_audit_generates_event_id(tmp_path, monkeypatch):
    from app.services import audit
    monkeypatch.setattr(audit, "AUDIT_FILE", tmp_path / "audit.jsonl")
    event_id = log_event("test", {"status": "ok"})
    assert len(event_id) == 64
    assert audit.AUDIT_FILE.exists()
