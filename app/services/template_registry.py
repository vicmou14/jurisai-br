from __future__ import annotations

from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"
TEMPLATES = {
    "coder": TEMPLATE_DIR / "template_coder.docx",
    "office": TEMPLATE_DIR / "template_escritorio.docx",
}


def template_for_profile(profile: str) -> Path:
    key = "coder" if profile == "coder" else "office"
    path = TEMPLATES[key]
    if not path.exists():
        raise FileNotFoundError(f"Template DOCX não encontrado: {path.name}")
    return path
