from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "legal_documents.jsonl"


def ensure_store() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.touch(exist_ok=True)


def save_document(document: dict[str, Any]) -> None:
    ensure_store()
    with DATA_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(document, ensure_ascii=False) + "\n")


def load_documents() -> list[dict[str, Any]]:
    ensure_store()
    documents: list[dict[str, Any]] = []
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                documents.append(json.loads(line))
    return documents
