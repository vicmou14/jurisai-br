from __future__ import annotations
import re
from app.services.classifier import DISCLAIMER, classify_text

DATE_RE = re.compile(r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b")
VALUE_RE = re.compile(r"(?:R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?|\b\d+[,.]\d{2}\b)")
PARTY_RE = re.compile(r"\b(?:Autor|Autora|Réu|Ré|Requerente|Requerido|Parte autora|Parte ré)\s*[:\-]\s*([^\n;,.]+)", re.I)

RISK_PATTERNS = [
    ("Prazo processual mencionado; confirme imediatamente a data e a forma de contagem.", ("prazo", "dias úteis", "intimação", "audiência")),
    ("Possível risco financeiro identificado; confirme valores, encargos e obrigações.", ("multa", "juros", "penalidade", "débito", "cobrança")),
    ("Possível situação urgente; procure atendimento profissional adequado.", ("prisão", "ameaça", "violência", "liminar")),
]

def _summary(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= 420:
        return cleaned
    return cleaned[:417].rstrip() + "..."

def analyze_document(text: str) -> dict:
    area, confidence, _ = classify_text(text)
    lower = text.lower()
    risks = [message for message, triggers in RISK_PATTERNS if any(t in lower for t in triggers)]
    return {
        "area": area,
        "confidence": confidence,
        "summary": _summary(text),
        "parties": [m.strip() for m in PARTY_RE.findall(text)][:10],
        "dates": DATE_RE.findall(text)[:20],
        "values": VALUE_RE.findall(text)[:20],
        "risks": risks or ["Nenhum alerta automático relevante identificado."],
        "disclaimer": DISCLAIMER,
    }
