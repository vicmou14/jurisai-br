from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from urllib.request import Request, urlopen

from app.connectors.base import ExternalLegalDocument, LegalSourceConnector


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text:
            self.parts.append(text)


class PlanaltoConnector(LegalSourceConnector):
    """Ingestão rastreável de páginas canônicas da legislação oficial."""

    name = "planalto"
    base_url = "https://www.planalto.gov.br/ccivil_03/"

    def fetch_url(self, url: str, category: str = "legislacao") -> ExternalLegalDocument:
        request = Request(url, headers={"User-Agent": "JurisAI-BR/1.0 legal-research"})
        with urlopen(request, timeout=30) as response:
            raw = response.read()
            final_url = response.geturl()
        html = raw.decode("latin-1", errors="replace")
        parser = _TextExtractor()
        parser.feed(html)
        content = "\n".join(parser.parts)
        title = parser.parts[0] if parser.parts else final_url
        digest = sha256(raw).hexdigest()
        return ExternalLegalDocument(
            title=title[:500],
            content=content,
            source=f"{final_url}#sha256={digest}",
            category=category,
            external_id=digest,
        )

    def fetch(self, query: str | None = None):
        if not query:
            return iter(())
        return iter((self.fetch_url(query),))
