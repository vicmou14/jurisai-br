from __future__ import annotations

import argparse

from app.services.sync import run_sync
from app.services.sync_state import mark_synced


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", choices=["stj", "planalto", "stf"])
    args = parser.parse_args()

    def job():
        # Source-specific ingestion is intentionally delegated to validated adapters.
        return (0, 0)

    result = run_sync(args.source, job)
    if not result.errors:
        mark_synced(args.source, result.finished_at)
    print(result)

if __name__ == "__main__":
    main()
