from __future__ import annotations

from app.connectors.base import ExternalLegalDocument, LegalSourceConnector

class STJConnector(LegalSourceConnector):
    name = "stj"
    base_url = "https://www.stj.jus.br/"

    def fetch(self, query: str | None = None):
        raise NotImplementedError(
            "A integração de jurisprudência do STJ deve ser implementada por adaptador específico, "
            "com metadados e verificação da fonte oficial."
        )
