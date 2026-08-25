from fastapi import Depends, FastAPI
from app.schemas import (
    ClassifyRequest, ClassificationResult, DocumentAnalysisRequest,
    DocumentAnalysisResult, LegalQueryRequest, LegalQueryResult,
)
from app.services.auth import require_api_key
from app.services.audit import log_event
from app.services.classifier import DISCLAIMER, classify_text, next_steps
from app.services.analyzer import analyze_document
from app.services.advisor import answer_question
from app.services.rag import answer_with_sources
from app.services.official_sources import list_official_sources
from app.services.search import semantic_search

app = FastAPI(
    title="JurisAI-BR",
    description="API de triagem, organização, pesquisa e recuperação de informações jurídicas brasileiras.",
    version="1.2.0",
)

@app.get("/")
def root() -> dict[str, str]:
    return {"name": "JurisAI-BR", "status": "online", "version": "1.2.0"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/v1/classify", response_model=ClassificationResult)
def classify(payload: ClassifyRequest, actor: str = Depends(require_api_key)) -> ClassificationResult:
    area, confidence, keywords = classify_text(payload.text)
    result = ClassificationResult(
        area=area, confidence=confidence, matched_keywords=keywords,
        next_steps=next_steps(area), disclaimer=DISCLAIMER,
    )
    log_event("classify", {"actor": actor, "area": area, "text_length": len(payload.text)})
    return result

@app.post("/v1/analyze-document", response_model=DocumentAnalysisResult)
def analyze(payload: DocumentAnalysisRequest, actor: str = Depends(require_api_key)) -> DocumentAnalysisResult:
    result = DocumentAnalysisResult(**analyze_document(payload.text))
    log_event("analyze_document", {"actor": actor, "area": result.area, "text_length": len(payload.text)})
    return result

@app.post("/v1/legal-query", response_model=LegalQueryResult)
def legal_query(payload: LegalQueryRequest, actor: str = Depends(require_api_key)) -> LegalQueryResult:
    result = LegalQueryResult(**answer_question(payload.question, payload.context))
    log_event("legal_query", {"actor": actor, "area": result.area})
    return result

@app.post("/v1/legal-research")
def legal_research(payload: LegalQueryRequest, actor: str = Depends(require_api_key)) -> dict:
    result = answer_with_sources(payload.question, payload.context)
    log_event("legal_research", {"actor": actor, "area": result["area"], "sources": len(result["sources"])})
    return result

@app.get("/v1/search")
def search(query: str, actor: str = Depends(require_api_key)) -> dict:
    results = semantic_search(query)
    log_event("search", {"actor": actor, "results": len(results)})
    return {"query": query, "results": results}

@app.get("/v1/sources")
def sources() -> dict:
    return list_official_sources()
