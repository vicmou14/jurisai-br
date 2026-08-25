from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app.services.sync import SyncResult, run_sync

SyncJob = Callable[[], tuple[int, int]]

@dataclass(frozen=True)
class RegisteredSource:
    name: str
    job: SyncJob

class SyncRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, RegisteredSource] = {}

    def register(self, name: str, job: SyncJob) -> None:
        self._sources[name] = RegisteredSource(name=name, job=job)

    def names(self) -> list[str]:
        return sorted(self._sources)

    def execute(self, name: str) -> SyncResult:
        if name not in self._sources:
            raise KeyError(f"Fonte não registrada: {name}")
        source = self._sources[name]
        return run_sync(source.name, source.job)

    def execute_all(self) -> list[SyncResult]:
        return [self.execute(name) for name in self.names()]
