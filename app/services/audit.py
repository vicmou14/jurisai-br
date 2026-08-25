from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

AUDIT_FILE = Path(__file__).resolve().parents[1] / "data" / "audit.jsonl"


def log_event(event: str, payload: dict) -> str:
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    canonical = json.dumps(record, ensure_ascii=False, sort_keys=True)
    record["id"] = sha256(canonical.encode("utf-8")).hexdigest()
    with AUDIT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record["id"]
