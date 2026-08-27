# JurisAI-BR

Ambiente pessoal para instruções, documentos e produção jurídica brasileira.

## Capacidades
- Recebe instruções diretas para elaboração de peças.
- Identifica automaticamente o perfil **Escritório** ou **CODER**.
- Ingestão de documentos em PDF e DOCX.
- Geração local gratuita com **Ollama + Qwen3:8B**.
- Integração opcional com OpenAI.
- Exportação para DOCX usando os templates timbrados:
  - `templates/template_escritorio.docx`
  - `templates/template_coder.docx`
- Triagem, pesquisa semântica, auditoria e conectores jurídicos.
- Interface web servida em `/web/`.

## Execução local no Windows

Pré-requisito já confirmado neste ambiente: `ollama list` deve mostrar `qwen3:8b`.

### 1. Obtenha ou atualize o projeto
```powershell
cd $HOME
if (-not (Test-Path jurisai-br)) { git clone https://github.com/vicmou14/jurisai-br.git }
cd jurisai-br
git pull
```

### 2. Execute o inicializador automático
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\start_local.ps1
```

O script verifica o Ollama e o modelo `qwen3:8b`, cria o ambiente Python, instala as dependências, cria `.env` quando necessário e inicia a API. A interface abre em:

`http://127.0.0.1:8000/web/`

## Verificação do gerador local
Com a API em execução, abra outro PowerShell e execute:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/v1/text/status
```

O resultado esperado inclui:

```text
provider       : ollama
model          : qwen3:8b
reachable      : True
model_available: True
```

## Produção com PostgreSQL e Docker
1. Copie `.env.example` para `.env` e defina os segredos e URLs de produção.
2. Ajuste `DATABASE_URL` e `JURISAI_OLLAMA_URL` conforme a infraestrutura.
3. Suba a infraestrutura:
```bash
docker compose up --build -d
```
4. Aplique `migrations/001_pgvector.sql` antes de habilitar consultas vetoriais nativas.
5. Reindexe documentos existentes:
```bash
python scripts/reindex_documents.py
```

## API principal
- `GET /v1/text/status` — verifica o provedor e o modelo configurado.
- `POST /v1/draft/prepare` — identifica perfil e tipo de peça.
- `POST /v1/draft/write` — gera o texto jurídico.
- `POST /v1/draft/export` — retorna a peça em DOCX timbrado.
- `POST /v1/documents/upload` — recebe PDF ou DOCX.

## Sincronização de fontes
- **STJ:** catálogo oficial de Dados Abertos via CKAN.
- **Planalto:** URLs canônicas em `JURISAI_PLANALTO_URLS`.
- **STF:** CSV exportado oficialmente em `JURISAI_STF_CSV`.

## Testes
```bash
pytest -q
```

## Segurança e LGPD
Use HTTPS e segredos fortes em produção, restrinja `JURISAI_CORS_ORIGINS`, faça backups e não trate dados reais de clientes sem revisão de privacidade, segurança e conformidade.

## Limites
O JurisAI-BR auxilia pesquisa, triagem e produção de rascunhos. A validação jurídica final, dos fatos, dos documentos e das fontes permanece sob responsabilidade do profissional responsável.
