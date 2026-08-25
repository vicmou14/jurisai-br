# Persistência e busca jurídica

## Fluxo atual
1. Um documento é enviado para `POST /v1/documents`.
2. O documento recebe um identificador determinístico.
3. O conteúdo é persistido no banco configurado por `DATABASE_URL`.
4. `GET /v1/search` executa ranking por similaridade sobre os documentos persistidos.

## Desenvolvimento
Sem `DATABASE_URL`, o projeto usa SQLite local. Para PostgreSQL:

```text
DATABASE_URL=postgresql+psycopg://jurisai:jurisai@localhost:5432/jurisai
```

O `docker-compose.yml` fornece uma instância PostgreSQL com pgvector para a próxima evolução.

## Próxima evolução
A interface de similaridade atual deve ser substituída por embeddings densos persistidos em uma coluna vetorial do PostgreSQL, com índice apropriado e metadados de versão do modelo.
