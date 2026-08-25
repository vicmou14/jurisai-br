#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Uso: $0 arquivo.sql.gz" >&2
  exit 1
fi
if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL não configurada" >&2
  exit 1
fi

gunzip -c "$1" | psql "$DATABASE_URL"
echo "Restauração concluída"
