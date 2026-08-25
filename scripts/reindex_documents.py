from sqlalchemy import select
from app.db import SessionLocal
from app.models import LegalDocument
from app.services.vector_index import index_text


def main() -> None:
    with SessionLocal() as session:
        documents = list(session.scalars(select(LegalDocument)))
        for document in documents:
            # The database vector column is introduced by the deployment migration.
            index_text(f"{document.title}\n{document.content}")
        print(f"Reindexed {len(documents)} document(s).")

if __name__ == "__main__":
    main()
