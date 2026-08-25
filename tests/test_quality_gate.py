from app.services.quality_gate import apply_quality_gate


def test_quality_gate_marks_grounded_result():
    result = apply_quality_gate({"sources": [{"title": "Fonte"}]})
    assert result["grounded"] is True
    assert result["source_count"] == 1


def test_quality_gate_marks_missing_sources():
    result = apply_quality_gate({"sources": []})
    assert result["grounded"] is False
    assert result["source_count"] == 0
