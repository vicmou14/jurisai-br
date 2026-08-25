from io import BytesIO

from app.connectors.stf_csv import STFCsvConnector


def test_reads_official_export_shape():
    raw = BytesIO("processo,ementa,url\nRE 1,Texto da ementa,https://portal.stf.jus.br/x\n".encode("utf-8"))
    documents = list(STFCsvConnector().read_stream(raw))
    assert len(documents) == 1
    assert documents[0].category == "jurisprudencia_stf"
    assert documents[0].external_id == "RE 1"
