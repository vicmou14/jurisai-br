from __future__ import annotations

import os
from fastapi import Header, HTTPException, status


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    configured_key = os.getenv("JURISAI_API_KEY")
    if not configured_key:
        return "development"
    if not x_api_key or x_api_key != configured_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida ou ausente.",
        )
    return "api-key"
