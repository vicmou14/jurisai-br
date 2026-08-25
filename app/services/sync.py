from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

@dataclass
class SyncResult:
    source: str
    started_at: str
    finished_at: str
    imported: int
    skipped: int
    errors: list[str]


def run_sync(source: str, job: Callable[[], tuple[int, int]]) -> SyncResult:
    started = datetime.now(timezone.utc).isoformat()
    errors: list[str] = []
    imported = skipped = 0
    try:
        imported, skipped = job()
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
    finished = datetime.now(timezone.utc).isoformat()
    return SyncResult(source, started, finished, imported, skipped, errors)
