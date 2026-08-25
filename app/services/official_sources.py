from __future__ import annotations

OFFICIAL_PORTALS = {
    "legislation": [
        {"name": "Planalto", "purpose": "Legislação federal e atos oficiais", "url": "https://www.planalto.gov.br/ccivil_03/"},
        {"name": "Câmara dos Deputados", "purpose": "Projetos e atividade legislativa", "url": "https://www.camara.leg.br/"},
        {"name": "Senado Federal", "purpose": "Atividade legislativa e normas", "url": "https://www12.senado.leg.br/"},
    ],
    "jurisprudence": [
        {"name": "STF", "purpose": "Jurisprudência e decisões do Supremo Tribunal Federal", "url": "https://portal.stf.jus.br/"},
        {"name": "STJ", "purpose": "Jurisprudência e decisões do Superior Tribunal de Justiça", "url": "https://www.stj.jus.br/"},
        {"name": "CNJ", "purpose": "Informações institucionais e serviços do Poder Judiciário", "url": "https://www.cnj.jus.br/"},
    ],
}

def list_official_sources() -> dict:
    return OFFICIAL_PORTALS
