# JurisAI-BR

Plataforma de triagem, pesquisa e organização de informações jurídicas brasileiras.

## Capacidades
- Triagem e análise inicial de documentos.
- Pesquisa semântica sobre documentos persistidos.
- Embeddings persistidos e arquitetura para pgvector.
- Ingestão de TXT, PDF e DOCX.
- Conectores STJ, Planalto e STF conforme os mecanismos oficiais configurados.
- Sincronização, deduplicação, auditoria e status de fontes.
- Interface web servida em `/web/`.
- Autenticação por API key e CORS configurável.

## Execução local
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abra `http://localhost:8000/web/`.

## Produção com PostgreSQL
1. Copie `.env.example` para `.env` e defina segredos reais.
2. Suba a infraestrutura:
```bash
docker compose up --build -d
```
3. Aplique `migrations/001_pgvector.sql` no PostgreSQL antes de habilitar consultas vetoriais nativas.
4. Reindexe documentos existentes:
```bash
python scripts/reindex_documents.py
```

## Sincronização de fontes
- **STJ:** catálogo oficial de Dados Abertos via CKAN.
- **Planalto:** URLs canônicas em `JURISAI_PLANALTO_URLS`.
- **STF:** CSV exportado oficialmente em `JURISAI_STF_CSV`.

API: `GET /v1/sync/status` e `POST /v1/sync/{stj|planalto|stf}`.

## Testes
```bash
pytest -q
```

## Segurança e LGPD
Use HTTPS e segredos fortes, restrinja `JURISAI_CORS_ORIGINS`, faça backups e não trate dados reais de clientes sem revisão de privacidade, segurança e conformidade. Em `JURISAI_ENV=production`, a ausência de API key bloqueia o acesso protegido.

## Limites
O JurisAI-BR auxilia pesquisa, triagem e organização. Não substitui análise jurídica profissional nem a validação humana e consulta às fontes oficiais atualizadas.
