# JurisAI-BR

Plataforma de triagem e organização de informações jurídicas brasileiras.

## O que a versão 1.0 faz

- Classifica textos em áreas jurídicas: civil, consumidor, trabalhista, família, criminal, tributário, previdenciário, administrativo e empresarial.
- Faz análise inicial de documentos, identificando datas, valores, partes e alertas automáticos.
- Recebe perguntas para triagem e sugere próximos passos e documentos relevantes.
- Expõe uma API HTTP com documentação automática em `/docs`.
- Inclui testes automatizados e CI com GitHub Actions.

## Execução

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse `http://127.0.0.1:8000/docs`.

## Endpoints

- `GET /health`
- `POST /v1/classify`
- `POST /v1/analyze-document`
- `POST /v1/legal-query`

## Exemplo

```bash
curl -X POST http://127.0.0.1:8000/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"Comprei um produto com defeito e a loja recusou a garantia."}'
```

## Limites

O JurisAI-BR realiza triagem e organização de informações. Não substitui análise profissional, consulta integral da legislação, jurisprudência atualizada ou atendimento de emergência.
