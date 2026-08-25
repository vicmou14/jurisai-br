import argparse

from app.db import Base, SessionLocal, engine
import app.models  # noqa: F401
from app.connectors.stf_csv import STFCsvConnector
from app.services.ingestion import ingest_external


def main() -> None:
    parser = argparse.ArgumentParser(description="Importa CSV oficial exportado do STF.")
    parser.add_argument("csv_file")
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    connector = STFCsvConnector()
    session = SessionLocal()
    imported = 0
    try:
        for document in connector.read_file(args.csv_file):
            ingest_external(session, document)
            imported += 1
    finally:
        session.close()
    print(f"Importados: {imported}")


if __name__ == "__main__":
    main()
