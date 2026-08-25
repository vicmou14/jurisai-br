CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE legal_documents
    ADD COLUMN IF NOT EXISTS embedding_vector vector(256);

CREATE INDEX IF NOT EXISTS legal_documents_embedding_vector_idx
ON legal_documents USING ivfflat (embedding_vector vector_cosine_ops)
WITH (lists = 100);
