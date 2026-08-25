from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class ExternalLegalDocument:
    title: str
    content: str
    source: str
    category: str
    external_id: str | None = None

class LegalSourceConnector(ABC):
    name: str

    @abstractmethod
    def fetch(self, query: str | None = None) -> Iterable[ExternalLegalDocument]:
        raise NotImplementedError
