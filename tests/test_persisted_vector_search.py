from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.services.document_repository import save_document
from app.services.semantic_search import search


def test_ingestion_persists_embedding_and_searches_it():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    document = save_document(session, "CDC", "Produto defeituoso adquirido por consumidor.", "teste", "consumidor")
    assert document.embedding
    assert document.embedding_dimensions == 256
    results = search(session, "consumidor produto defeituoso")
    assert results
    assert results[0]["id"] == document.id
