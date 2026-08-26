from app.services.draft_generation import build_draft_request


def test_coder_profile_is_selected_for_coder_document():
    result = build_draft_request("Elabore uma contestação para a CODER", documents=[])
    assert result["profile"] == "coder"
    assert result["document_type"] == "contestacao"
    assert "Do mérito" in result["sections"]


def test_office_profile_is_default():
    result = build_draft_request("Faça uma petição inicial", documents=[])
    assert result["profile"] == "office"
    assert result["document_type"] == "peticao_inicial"
