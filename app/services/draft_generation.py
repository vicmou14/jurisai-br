from __future__ import annotations

from app.services.writing_profiles import build_writing_brief

SECTION_MAP = {
    "peticao_inicial": ["Endereçamento", "Qualificação das partes", "Dos fatos", "Do direito", "Dos pedidos", "Provas", "Valor da causa", "Requerimentos finais"],
    "contestacao": ["Endereçamento", "Síntese da demanda", "Preliminares", "Do mérito", "Impugnação dos fatos e provas", "Dos pedidos"],
    "manifestacao": ["Endereçamento", "Síntese do ponto submetido", "Dos fatos e documentos", "Da fundamentação", "Do pedido"],
    "replica": ["Endereçamento", "Síntese da contestação", "Da impugnação específica", "Das provas", "Dos pedidos"],
    "recurso": ["Endereçamento", "Tempestividade e cabimento", "Síntese da decisão recorrida", "Das razões recursais", "Do pedido de reforma"],
    "oficio": ["Destinatário", "Assunto", "Referência", "Exposição objetiva", "Providência ou solicitação", "Encerramento institucional"],
    "parecer": ["Relatório", "Questão jurídica", "Fundamentação", "Análise dos riscos", "Conclusão"],
    "habeas_corpus": ["Endereçamento", "Identificação do paciente", "Síntese da coação", "Do cabimento", "Do constrangimento ilegal", "Do pedido liminar e final"],
    "peticao": ["Endereçamento", "Contextualização", "Fundamentação", "Pedidos"],
    "documento_juridico": ["Identificação do documento", "Contexto", "Fundamentação", "Conclusão ou pedido"],
}


def build_draft_request(instruction: str, context: str | None = None, documents: list[dict] | None = None) -> dict:
    brief = build_writing_brief(instruction, context)
    sections = SECTION_MAP[brief["document_type"]]
    attached = documents or []
    document_text = "\n\n".join(
        f"DOCUMENTO: {item.get('title', 'Sem título')}\n{item.get('content', '').strip()}"
        for item in attached
        if str(item.get("content") or "").strip()
    )
    generation_instructions = [
        f"Produza uma {brief['document_type'].replace('_', ' ')} completa, no perfil {brief['profile_name']}.",
        *brief["rules"],
        "Utilize exclusivamente os fatos, documentos e dados efetivamente fornecidos como base factual.",
        "Quando faltar informação essencial, não invente: sinalize a lacuna com [INFORMAÇÃO NECESSÁRIA].",
        "Mantenha a coerência cronológica e a correspondência entre alegação, documento e pedido.",
    ]
    return {
        **brief,
        "sections": sections,
        "documents_count": len(attached),
        "documents_context": document_text,
        "generation_instructions": generation_instructions,
    }
