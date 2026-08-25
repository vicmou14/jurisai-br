from fastapi import FastAPI
from app.schemas import (
    ClassifyRequest, ClassificationResult, DocumentAnalysisRequest,
    DocumentAnalysisResult, LegalQueryRequest, LegalQueryResult,
)
from app.services.classifier import DISCLAIMER, classify_text, next_steps
from app.services.analyzer import analyze_document
from app.services.advisor import answer_question

app = FastAPI(
    title="JurisAI-BR",
    description="API de triagem e organização de informações jurídicas brasileiras.",
    version="1.0.0",
)

@app.get("/")
def root() -> dict[str, str]:
    return {"name": "JurisAI-BR", "status": "online", "version": "1.0.0"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/v1/classify", response_model=ClassificationResult)
def classify(payload: ClassifyRequest) -> ClassificationResult:
    area, confidence, keywords = classify_text(payload.text)
    return ClassificationResult(
        area=area, confidence=confidence, matched_keywords=keywords,
        next_steps=next_steps(area), disclaimer=DISCLAIMER,
    )

@app.post("/v1/analyze-document", response_model=DocumentAnalysisResult)
def analyze(payload: DocumentAnalysisRequest) -> DocumentAnalysisResult:
    return DocumentAnalysisResult(**analyze_document(payload.text))

@app.post("/v1/legal-query", response_model=LegalQueryResult)
def legal_query(payload: LegalQueryRequest) -> LegalQueryResult:
    return LegalQueryResult(**answer_question(payload.question, payload.context))
