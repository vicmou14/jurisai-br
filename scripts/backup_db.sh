#!/usr/bin/env sh
set -eu

BACKUP_DIR="${BACKUP_DIR:-./backups}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$BACKUP_DIR"

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL não configurada" >&2
  exit 1
fi

pg_dump "$DATABASE_URL" | gzip > "$BACKUP_DIR/jurisai-$STAMP.sql.gz"
echo "Backup criado: $BACKUP_DIR/jurisai-$STAMP.sql.gz"
