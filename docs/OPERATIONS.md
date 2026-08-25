# Operações do JurisAI-BR

## Verificação

- `GET /health`: processo ativo.
- `GET /ready`: aplicação e banco prontos.
- `GET /health/details`: diagnóstico básico.

## Backup

Configure `DATABASE_URL` e execute:

```sh
sh scripts/backup_db.sh
```

## Restauração

```sh
DATABASE_URL=... sh scripts/restore_db.sh backups/arquivo.sql.gz
```

## Produção

1. Defina `JURISAI_ENV=production`.
2. Defina uma `JURISAI_API_KEY` forte.
3. Defina `POSTGRES_PASSWORD` fora do repositório.
4. Restrinja `JURISAI_CORS_ORIGINS` aos domínios efetivamente utilizados.
5. Configure backup periódico e teste restaurações.
6. Monitore `/ready` e erros do serviço.
