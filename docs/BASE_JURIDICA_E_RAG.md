# Base jurídica e RAG

## Objetivo
A versão 1.1 adiciona uma camada de recuperação de informações jurídicas antes da geração da resposta.

## Estado atual
- Base local demonstrativa para validação técnica.
- Catálogo de portais oficiais para legislação e jurisprudência.
- Endpoint `/v1/legal-research` que retorna área jurídica, confiança e fontes recuperadas.

## Produção
Antes de uso profissional, a base deve ser alimentada por dados obtidos de fontes oficiais, com:
1. versionamento e data de atualização;
2. identificação da fonte primária;
3. validação da vigência normativa;
4. metadados de tribunal, órgão, data e processo para jurisprudência;
5. mecanismo de citação e rastreabilidade;
6. revisão jurídica humana para respostas de maior risco.

## Observação
O catálogo de fontes não substitui um conector de atualização automática. Uma integração de produção deve respeitar APIs, termos de uso, limites de acesso e regras de cada órgão.
