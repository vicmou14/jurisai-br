from __future__ import annotations
from app.services.classifier import DISCLAIMER, classify_text, next_steps

DOCS = {
    "consumidor": ["nota fiscal", "contrato", "protocolos de atendimento", "comprovantes"],
    "trabalhista": ["CTPS", "contracheques", "contrato", "registros de jornada"],
    "familia": ["documentos pessoais", "certidões", "comprovantes financeiros", "provas relevantes"],
    "criminal": ["documentos do procedimento", "provas disponíveis", "intimações"],
    "previdenciario": ["CNIS", "laudos", "documentos de identidade", "comprovantes do benefício"],
}

def answer_question(question: str, context: str | None = None) -> dict:
    combined = question + ("\n" + context if context else "")
    area, confidence, _ = classify_text(combined)
    steps = next_steps(area)
    if area == "desconhecida":
        answer = "Não foi possível identificar com segurança uma área jurídica predominante. Informe fatos, datas, local e documentos existentes para uma triagem melhor."
    else:
        answer = f"A triagem automática indica possível relação com direito {area}. Próximos passos sugeridos: " + " ".join(steps)
    return {
        "area": area,
        "confidence": confidence,
        "answer": answer,
        "suggested_documents": DOCS.get(area, ["documentos pessoais", "contratos ou comunicações relevantes", "cronologia dos fatos"]),
        "disclaimer": DISCLAIMER,
    }
