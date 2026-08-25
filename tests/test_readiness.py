from app.services.readiness import database_ready


def test_database_ready_returns_tuple():
    result = database_ready()
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
