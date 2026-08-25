from __future__ import annotations
import re
from collections import Counter

AREA_KEYWORDS: dict[str, tuple[str, ...]] = {
    "civil": ("contrato", "indenização", "danos morais", "responsabilidade civil", "obrigação", "cobrança", "aluguel", "locação"),
    "consumidor": ("consumidor", "produto", "defeito", "compra", "fornecedor", "garantia", "propaganda", "cancelamento"),
    "trabalhista": ("trabalho", "empregado", "empregador", "demissão", "fgts", "horas extras", "salário", "rescisão"),
    "familia": ("divórcio", "guarda", "pensão", "alimentos", "união estável", "inventário", "herança", "partilha"),
    "criminal": ("crime", "delegacia", "boletim de ocorrência", "prisão", "inquérito", "acusado", "furto", "ameaça"),
    "tributario": ("imposto", "tributo", "receita federal", "icms", "iss", "iptu", "execução fiscal", "multa tributária"),
    "previdenciario": ("inss", "aposentadoria", "benefício", "auxílio-doença", "bpc", "previdência", "perícia"),
    "administrativo": ("licitação", "servidor público", "concurso", "administração pública", "processo administrativo", "ato administrativo"),
    "empresarial": ("empresa", "sociedade", "sócio", "falência", "recuperação judicial", "contrato social", "cnpj"),
}

NEXT_STEPS = {
    "civil": ["Organize contratos, mensagens e comprovantes.", "Registre cronologia dos fatos e prejuízos."],
    "consumidor": ["Guarde nota fiscal, contrato e protocolos.", "Registre reclamações feitas ao fornecedor."],
    "trabalhista": ["Separe holerites, contrato e registros de jornada.", "Anote datas relevantes da relação de trabalho."],
    "familia": ["Organize documentos pessoais e provas relevantes.", "Evite decisões urgentes sem orientação profissional."],
    "criminal": ["Preserve provas e documentos sem alterá-los.", "Procure orientação jurídica imediatamente em situações urgentes."],
    "tributario": ["Separe notificações e documentos fiscais.", "Observe os prazos indicados em intimações."],
    "previdenciario": ["Separe CNIS, laudos e documentos médicos quando aplicável.", "Verifique comunicações e prazos do órgão responsável."],
    "administrativo": ["Guarde o processo e as comunicações oficiais.", "Verifique prazo para defesa ou recurso."],
    "empresarial": ["Organize contratos e documentos societários.", "Mapeie obrigações, prazos e impactos financeiros."],
    "desconhecida": ["Descreva melhor os fatos, datas e documentos disponíveis.", "Busque orientação profissional para classificação do caso."],
}

DISCLAIMER = "Informação jurídica geral e automatizada; não substitui análise de advogado ou órgão competente."

def classify_text(text: str) -> tuple[str, float, list[str]]:
    normalized = re.sub(r"\s+", " ", text.lower())
    hits: dict[str, list[str]] = {}
    for area, keywords in AREA_KEYWORDS.items():
        found = [kw for kw in keywords if kw in normalized]
        if found:
            hits[area] = found
    if not hits:
        return "desconhecida", 0.0, []
    ranked = Counter({area: len(words) for area, words in hits.items()})
    area, score = ranked.most_common(1)[0]
    confidence = min(0.95, round(0.35 + score * 0.18, 2))
    return area, confidence, hits[area]

def next_steps(area: str) -> list[str]:
    return NEXT_STEPS.get(area, NEXT_STEPS["desconhecida"])
