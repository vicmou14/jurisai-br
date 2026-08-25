from __future__ import annotations

import os
import secrets
from fastapi import Header, HTTPException, status


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    configured_key = os.getenv("JURISAI_API_KEY")
    environment = os.getenv("JURISAI_ENV", "development").lower()
    if not configured_key:
        if environment == "production":
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Autenticação não configurada.")
        return "development"
    if not x_api_key or not secrets.compare_digest(x_api_key, configured_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida ou ausente.")
    return "api-key"
