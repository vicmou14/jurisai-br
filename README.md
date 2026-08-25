# JurisAI-BR

Plataforma de triagem, pesquisa e organização de informações jurídicas brasileiras.

## Capacidades

- Triagem por áreas jurídicas.
- Análise inicial de documentos.
- Perguntas jurídicas e recuperação de fontes.
- Persistência de documentos com SQLAlchemy.
- Busca ranqueada sobre a base persistida.
- Auditoria e autenticação por API key.
- Sincronização de fontes jurídicas oficiais.
- Interface web para pesquisa e ingestão.

## Execução rápida

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Para desenvolvimento com PostgreSQL/pgvector:

```bash
docker compose up -d
export DATABASE_URL='postgresql+psycopg://jurisai:jurisai@localhost:5432/jurisai'
uvicorn app.main:app --reload
```

## Sincronização de fontes

O projeto sincroniza apenas pelos adaptadores implementados e configurados:

- **STJ:** catálogo oficial de Dados Abertos via CKAN.
- **Planalto:** URLs canônicas oficiais configuradas em `JURISAI_PLANALTO_URLS`.
- **STF:** CSV exportado pela pesquisa oficial, configurado em `JURISAI_STF_CSV`.

Exemplos:

```bash
export JURISAI_PLANALTO_URLS='https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm'
export JURISAI_STF_CSV='./dados/stf.csv'
python scripts/sync_sources.py planalto
python scripts/sync_sources.py stf
```

A API também expõe:

- `GET /v1/sync/status`
- `POST /v1/sync/stj`
- `POST /v1/sync/planalto`
- `POST /v1/sync/stf`

## Testes

```bash
pytest -q
```

## Limites

O JurisAI-BR realiza pesquisa, triagem e organização de informações. Não substitui análise jurídica profissional, consulta integral e atualizada das fontes oficiais, nem validação humana antes do uso em casos concretos.
