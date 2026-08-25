from __future__ import annotations

from urllib.parse import urlencode
from urllib.request import urlopen
import json

from app.connectors.base import ExternalLegalDocument, LegalSourceConnector


class STJConnector(LegalSourceConnector):
    """Cliente para o catálogo oficial CKAN de dados abertos do STJ."""

    name = "stj"
    api_base = "https://dadosabertos.web.stj.jus.br/api/3/action"

    def _get(self, action: str, **params) -> dict:
        query = urlencode(params)
        url = f"{self.api_base}/{action}" + (f"?{query}" if query else "")
        with urlopen(url, timeout=30) as response:
            payload = json.load(response)
        if not payload.get("success"):
            raise RuntimeError(f"CKAN API error: {action}")
        return payload["result"]

    def search_datasets(self, query: str = "jurisprudencia", rows: int = 20) -> list[dict]:
        result = self._get("package_search", q=query, rows=rows)
        return result.get("results", [])

    def dataset(self, dataset_id: str) -> dict:
        return self._get("package_show", id=dataset_id)

    def fetch(self, query: str | None = None):
        for dataset in self.search_datasets(query or "jurisprudencia"):
            yield ExternalLegalDocument(
                title=dataset.get("title") or dataset["name"],
                content=dataset.get("notes") or "",
                source=dataset.get("url") or f"STJ Dados Abertos: {dataset['name']}",
                category="jurisprudencia",
                external_id=dataset.get("id"),
            )

    def list_resources(self, dataset_id: str) -> list[dict]:
        return self.dataset(dataset_id).get("resources", [])
