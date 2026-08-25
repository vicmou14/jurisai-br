from app.services.classifier import classify_text
from app.services.knowledge_base import retrieve

DISCLAIMER = "Resposta informativa para triagem. Não substitui análise de advogado(a) ou órgão competente."

def answer_with_sources(question: str, context: str | None = None) -> dict:
    combined = f"{question} {context or ''}".strip()
    area, confidence, _ = classify_text(combined)
    sources = retrieve(combined)

    if sources:
        summary = "Foram encontrados materiais relacionados à pergunta. A aplicação deve confrontar os fatos do caso com a redação oficial e vigente das normas."
    else:
        summary = "Não foi encontrada uma referência suficientemente relacionada na base local demonstrativa."

    return {
        "answer": summary,
        "area": area,
        "confidence": confidence,
        "sources": sources,
        "disclaimer": DISCLAIMER,
    }
