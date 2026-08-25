from __future__ import annotations

from datetime import datetime, timezone

from app.services.sync_state import load_state


def status(source_names: list[str]) -> dict:
    state = load_state()
    now = datetime.now(timezone.utc).isoformat()
    return {
        "checked_at": now,
        "sources": [
            {
                "name": name,
                "last_success": state.get(name, {}).get("last_success"),
                "configured": name in {"stj", "planalto", "stf"},
            }
            for name in source_names
        ],
    }
