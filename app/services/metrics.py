from __future__ import annotations

from collections import Counter
from threading import Lock

_counts: Counter[str] = Counter()
_lock = Lock()


def increment(name: str) -> None:
    with _lock:
        _counts[name] += 1


def snapshot() -> dict[str, int]:
    with _lock:
        return dict(_counts)
