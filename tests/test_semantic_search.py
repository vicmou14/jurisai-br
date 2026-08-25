from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.services.document_repository import save_document
from app.services.semantic_search import search


def test_semantic_search_ranks_relevant_document():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    save_document(session, "CDC", "Consumidor comprou produto defeituoso e busca reparação.", "fonte", "consumidor")
    save_document(session, "CLT", "Trabalhador discute salário e jornada.", "fonte", "trabalhista")
    results = search(session, "produto com defeito para consumidor")
    assert results
    assert results[0]["category"] == "consumidor"
