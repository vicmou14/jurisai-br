from app.services.classifier import classify_text

def test_classifies_consumer_case():
    area, confidence, keywords = classify_text("Comprei um produto com defeito e a loja recusou a garantia.")
    assert area == "consumidor"
    assert confidence > 0
    assert "produto" in keywords

def test_classifies_labor_case():
    area, _, _ = classify_text("Fui demitido e não recebi corretamente FGTS e horas extras.")
    assert area == "trabalhista"

def test_unknown_case():
    area, confidence, keywords = classify_text("Preciso de uma análise geral sem detalhes suficientes.")
    assert area == "desconhecida"
    assert confidence == 0
    assert keywords == []
