from __future__ import annotations

from fastapi import HTTPException, Request

from app.services.rate_limit import limiter


def enforce_rate_limit(request: Request) -> None:
    client = request.client.host if request.client else "unknown"
    if not limiter.allow(client):
        raise HTTPException(status_code=429, detail="Limite temporário de requisições excedido.")
