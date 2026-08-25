from __future__ import annotations

import csv
from io import TextIOWrapper
from pathlib import Path
from typing import Iterable

from app.connectors.base import ExternalLegalDocument


class STFCsvConnector:
    """Ingests CSV files exported from the STF's official jurisprudence search."""

    name = "stf_csv"

    def read_file(self, path: str | Path) -> Iterable[ExternalLegalDocument]:
        with open(path, "rb") as raw:
            yield from self.read_stream(raw)

    def read_stream(self, raw) -> Iterable[ExternalLegalDocument]:
        text = TextIOWrapper(raw, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(text)
        for row in reader:
            normalized = {str(key or "").strip().lower(): (value or "").strip() for key, value in row.items()}
            title = self._first(normalized, "titulo", "ementa", "processo", "numero do processo") or "Jurisprudência STF"
            content = "\n".join(value for value in normalized.values() if value)
            if not content:
                continue
            source = self._first(normalized, "url", "link", "fonte") or "https://portal.stf.jus.br/"
            external_id = self._first(normalized, "id", "processo", "numero do processo")
            yield ExternalLegalDocument(
                title=title,
                content=content,
                source=source,
                category="jurisprudencia_stf",
                external_id=external_id or None,
            )

    @staticmethod
    def _first(row: dict[str, str], *keys: str) -> str:
        for key in keys:
            if row.get(key):
                return row[key]
        return ""
