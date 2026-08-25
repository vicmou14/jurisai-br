from fastapi import FastAPI
from app.schemas import (
    ClassifyRequest, ClassificationResult, DocumentAnalysisRequest,
    DocumentAnalysisResult, LegalQueryRequest, LegalQueryResult,
)
from app.services.classifier import DISCLAIMER, classify_text, next_steps
from app.services.analyzer import analyze_document
from app.services.advisor import answer_question
from app.services.rag import answer_with_sources
from app.services.official_sources import list_official_sources

app = FastAPI(
    title="JurisAI-BR",
    description="API de triagem, organização e recuperação de informações jurídicas brasileiras.",
    version="1.1.0",
)

@app.get("/")
def root() -> dict[str, str]:
    return {"name": "JurisAI-BR", "status": "online", "version": "1.1.0"}

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

@app.post("/v1/legal-research")
def legal_research(payload: LegalQueryRequest) -> dict:
    return answer_with_sources(payload.question, payload.context)

@app.get("/v1/sources")
def sources() -> dict:
    return list_official_sources()
