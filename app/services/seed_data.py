from app.services.document_repository import save_document
from app.services.knowledge_base import SOURCES


def seed_demo_data(session) -> int:
    count = 0
    for item in SOURCES:
        save_document(
            session,
            title=item.title,
            content=item.content,
            source=item.source,
            category=item.topics[0] if item.topics else "geral",
        )
        count += 1
    return count
