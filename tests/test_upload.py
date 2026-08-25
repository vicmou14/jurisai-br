from app.services.upload import extract_text


def test_extract_text_from_txt():
    assert extract_text("documento.txt", b"Texto juridico de teste") == "Texto juridico de teste"


def test_rejects_unknown_format():
    try:
        extract_text("documento.exe", b"x")
    except ValueError as exc:
        assert "Formato não suportado" in str(exc)
    else:
        raise AssertionError("Formato deveria ser rejeitado")
