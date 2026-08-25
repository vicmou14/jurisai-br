from __future__ import annotations

from app.connectors.base import ExternalLegalDocument, LegalSourceConnector

class PlanaltoConnector(LegalSourceConnector):
    name = "planalto"
    base_url = "https://www.planalto.gov.br/ccivil_03/"

    def fetch(self, query: str | None = None):
        raise NotImplementedError(
            "A coleta automática do Planalto exige um adaptador validado por fonte e versão normativa. "
            "Use a ingestão manual ou implemente um cliente específico com rastreabilidade."
        )
