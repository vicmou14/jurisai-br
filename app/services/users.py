from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import os

@dataclass(frozen=True)
class Principal:
    subject: str
    role: str

def authenticate_api_key(value: str | None) -> Principal:
    expected = os.getenv("JURISAI_API_KEY")
    if not expected:
        return Principal(subject="development", role="admin")
    if not value or value != expected:
        raise PermissionError("Credencial inválida")
    fingerprint = sha256(value.encode()).hexdigest()[:12]
    return Principal(subject=f"api:{fingerprint}", role="user")
