from __future__ import annotations

from app.services.sync_registry import SyncRegistry


def build_registry() -> SyncRegistry:
    registry = SyncRegistry()

    def pending(source: str):
        def job() -> tuple[int, int]:
            # Each validated connector replaces this placeholder with real ingestion.
            return (0, 0)
        return job

    registry.register("stj", pending("stj"))
    registry.register("planalto", pending("planalto"))
    registry.register("stf", pending("stf"))
    return registry
