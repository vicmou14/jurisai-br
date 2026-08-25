from __future__ import annotations

from app.connectors.base import ExternalLegalDocument, LegalSourceConnector

class STFConnector(LegalSourceConnector):
    name = "stf"
    base_url = "https://portal.stf.jus.br/"

    def fetch(self, query: str | None = None):
        raise NotImplementedError(
            "A integração de jurisprudência deve usar uma fonte oficial compatível e preservar metadados "
            "como tribunal, órgão julgador, data, classe e identificação do processo."
        )
