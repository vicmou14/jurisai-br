from app.services.sync import run_sync


def test_orchestrator_success_result():
    result = run_sync("stj", lambda: (2, 1))
    assert result.imported == 2
    assert result.skipped == 1
    assert result.errors == []


def test_orchestrator_records_failure():
    def job():
        raise ValueError("falha de integração")
    result = run_sync("planalto", job)
    assert result.errors
