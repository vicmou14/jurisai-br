from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import LegalDocument
from app.services.document_repository import save_document, search_documents


def test_save_and_search_document():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    document = save_document(
        session,
        title="CDC - produto defeituoso",
        content="Consumidor adquiriu produto com vício e busca reparação.",
        source="teste",
        category="consumidor",
    )
    assert document.id
    results = search_documents(session, "produto")
    assert len(results) == 1
