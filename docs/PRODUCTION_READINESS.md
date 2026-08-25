# Produção e segurança

## Implementado
- API key por variável de ambiente.
- Principal com identificador derivado sem registrar a chave bruta.
- Auditoria de operações.
- PostgreSQL e pgvector no ambiente Docker.
- Interface de embeddings de produção.
- Contratos para conectores jurídicos externos.

## Antes de produção
1. Configurar `DATABASE_URL` para PostgreSQL gerenciado.
2. Configurar segredo forte em `JURISAI_API_KEY` ou substituir por autenticação de usuários/OAuth.
3. Configurar CORS, HTTPS e proxy reverso.
4. Implementar provider real de embeddings e versionar o modelo.
5. Persistir vetores em pgvector com índice apropriado.
6. Implementar cada conector oficial com validação, limites, metadados e rastreabilidade.
7. Adicionar migrações de banco, backups, monitoramento e alertas.
8. Fazer revisão de segurança e LGPD antes do tratamento de dados reais de clientes.
