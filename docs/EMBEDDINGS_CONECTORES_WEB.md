# Embeddings, conectores e interface web

## Embeddings e pgvector
A versão atual introduz uma abstração de vetores. O baseline usa frequência de tokens para manter o projeto executável sem credenciais externas. Em produção, substitua por embeddings densos e persista vetores no PostgreSQL com pgvector.

## Conectores oficiais
Foi criada uma interface de conectores e um catálogo dos portais oficiais. Cada fonte precisa de um adaptador específico, respeitando API disponível, termos de uso, limites de acesso e formato dos dados. O projeto não deve raspar fontes de forma indiscriminada.

## Interface web
A interface em `web/` permite pesquisa e ingestão. Para publicação em produção, recomenda-se autenticação, gestão segura da API key, CORS configurado e um frontend com sessão de usuário.
