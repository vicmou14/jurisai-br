from app.services.rag import answer_with_sources
from app.services.official_sources import list_official_sources


def test_retrieves_consumer_source():
    result = answer_with_sources("Comprei um produto com defeito e quero reparação")
    assert result["sources"]
    assert result["area"] == "consumidor"


def test_official_source_catalog():
    result = list_official_sources()
    assert result["legislation"]
    assert result["jurisprudence"]
