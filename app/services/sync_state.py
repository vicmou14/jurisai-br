from __future__ import annotations

import json
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parents[1] / "data" / "sync_state.json"

def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))

def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def mark_synced(source: str, timestamp: str) -> None:
    state = load_state()
    state[source] = {"last_success": timestamp}
    save_state(state)
