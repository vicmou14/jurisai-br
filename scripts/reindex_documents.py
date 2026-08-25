from datetime import datetime, timezone
from sqlalchemy import select
from app.db import SessionLocal
from app.models import LegalDocument
from app.services.embedding_provider import get_provider


def main() -> None:
    provider = get_provider()
    with SessionLocal() as session:
        documents = list(session.scalars(select(LegalDocument)))
        for document in documents:
            document.embedding = provider.embed_one(f"{document.title}\n{document.content}")
            document.embedding_provider = provider.name
            document.embedding_dimensions = len(document.embedding)
            document.embedded_at = datetime.now(timezone.utc)
        session.commit()
        print(f"Reindexed {len(documents)} document(s) with {provider.name}.")

if __name__ == "__main__":
    main()
