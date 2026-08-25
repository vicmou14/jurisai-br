from app.services.source_ingestion import normalize_document
from app.services.retrieval import tokens


def test_normalize_document_is_traceable():
    document = normalize_document(
        "Fonte Oficial",
        "https://example.org/norma",
        "Norma de teste",
        "Conteúdo jurídico de teste",
        {"jurisdiction": "BR"},
    )
    assert document["id"]
    assert document["source_url"] == "https://example.org/norma"
    assert "retrieved_at" in document


def test_tokenization_handles_portuguese_text():
    assert "consumidor" in tokens("Proteção do consumidor contra cobrança indevida")
