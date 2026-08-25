from app.services.classifier import classify_text
from app.services.knowledge_base import retrieve
from app.services.quality_gate import apply_quality_gate

DISCLAIMER = "Resposta informativa para triagem e pesquisa. Não substitui análise de advogado(a), órgão competente ou revisão jurídica humana."


def answer_with_sources(question: str, context: str | None = None) -> dict:
    combined = f"{question} {context or ''}".strip()
    area, confidence, _ = classify_text(combined)
    sources = retrieve(combined)

    if sources:
        summary = "Foram encontrados materiais relacionados à pergunta. A aplicação deve confrontar os fatos do caso com a redação oficial e vigente das normas antes de qualquer conclusão."
    else:
        summary = "Não foi encontrada uma referência suficientemente relacionada. A consulta deve ser tratada como não fundamentada e requer pesquisa adicional em fonte oficial."

    return apply_quality_gate({
        "answer": summary,
        "area": area,
        "confidence": confidence,
        "sources": sources,
        "disclaimer": DISCLAIMER,
    })
