from __future__ import annotations

import os

from app.connectors.planalto import PlanaltoConnector
from app.connectors.stf_csv import STFCsvConnector
from app.connectors.stj import STJConnector
from app.db import SessionLocal
from app.services.ingestion import ingest_external
from app.services.sync_registry import SyncRegistry


def _ingest_documents(documents) -> tuple[int, int]:
    imported = skipped = 0
    with SessionLocal() as session:
        for document in documents:
            existed = session.get(__import__("app.models", fromlist=["LegalDocument"]).LegalDocument,
                                 __import__("app.services.document_repository", fromlist=["document_id"]).document_id(
                                     document.title, document.content, document.source))
            ingest_external(session, document)
            if existed:
                skipped += 1
            else:
                imported += 1
    return imported, skipped


def build_registry() -> SyncRegistry:
    registry = SyncRegistry()

    def stj_job() -> tuple[int, int]:
        query = os.getenv("JURISAI_STJ_QUERY", "jurisprudencia")
        rows = int(os.getenv("JURISAI_STJ_ROWS", "20"))
        return _ingest_documents(STJConnector().fetch(query=query))

    def planalto_job() -> tuple[int, int]:
        urls = [value.strip() for value in os.getenv("JURISAI_PLANALTO_URLS", "").split(",") if value.strip()]
        if not urls:
            return (0, 0)
        connector = PlanaltoConnector()
        return _ingest_documents(connector.fetch_url(url) for url in urls)

    def stf_job() -> tuple[int, int]:
        path = os.getenv("JURISAI_STF_CSV")
        if not path:
            return (0, 0)
        return _ingest_documents(STFCsvConnector().read_file(path))

    registry.register("stj", stj_job)
    registry.register("planalto", planalto_job)
    registry.register("stf", stf_job)
    return registry
