"""Ponto de partida para sincronização de fontes jurídicas oficiais.

Não baixa dados automaticamente nesta versão. Em produção, implemente conectores
por fonte, respeitando APIs, termos de uso, limites e requisitos de citação.
"""

from app.services.official_sources import list_official_sources


def main() -> None:
    for category, sources in list_official_sources().items():
        print(f"[{category}]")
        for source in sources:
            print(f"- {source['name']}: {source['url']}")


if __name__ == "__main__":
    main()
