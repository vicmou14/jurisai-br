from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_and_health():
    assert client.get("/").status_code == 200
    assert client.get("/health").json() == {"status": "ok"}

def test_classify_endpoint():
    response = client.post("/v1/classify", json={"text": "Meu empregador não pagou horas extras e meu FGTS está atrasado."})
    assert response.status_code == 200
    assert response.json()["area"] == "trabalhista"

def test_document_analysis():
    text = "Autor: João da Silva\nEm 10/08/2026 houve cobrança de R$ 1.250,00 com multa e prazo de 5 dias úteis."
    response = client.post("/v1/analyze-document", json={"text": text})
    body = response.json()
    assert response.status_code == 200
    assert "10/08/2026" in body["dates"]
    assert body["values"]
    assert body["risks"]

def test_legal_query():
    response = client.post("/v1/legal-query", json={"question": "Quais documentos devo guardar em uma disputa com uma loja por produto defeituoso?"})
    assert response.status_code == 200
    assert response.json()["area"] == "consumidor"

def test_validation_rejects_short_text():
    response = client.post("/v1/classify", json={"text": "curto"})
    assert response.status_code == 422
