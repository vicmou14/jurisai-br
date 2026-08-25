from app.services.vector_store import backend_info, score


def test_vector_score_prefers_related_text():
    related = score("produto defeituoso consumidor", "consumidor comprou produto defeituoso")
    unrelated = score("produto defeituoso consumidor", "jornada de trabalho e salário")
    assert related > unrelated


def test_vector_backend_info():
    assert backend_info()["pgvector_ready"] is True
