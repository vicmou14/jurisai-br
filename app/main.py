import os
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.db import Base, engine, get_session
import app.models  # noqa: F401
from app.schemas import ClassifyRequest, ClassificationResult, DocumentAnalysisRequest, DocumentAnalysisResult, LegalDocumentCreate, LegalQueryRequest, LegalQueryResult
from app.services.auth import require_api_key
from app.services.audit import log_event
from app.services.classifier import DISCLAIMER, classify_text, next_steps
from app.services.analyzer import analyze_document
from app.services.advisor import answer_question
from app.services.document_repository import save_document
from app.services.rag import answer_with_sources
from app.services.official_sources import list_official_sources
from app.services.readiness import database_ready
from app.services.seed_data import seed_demo_data
from app.services.semantic_search import search as semantic_document_search
from app.services.security import enforce_rate_limit
from app.services.sync_jobs import build_registry
from app.services.sync_state import load_state, mark_synced
from app.services.upload import extract_text

app = FastAPI(title="JurisAI-BR", description="API de triagem, organização, pesquisa e recuperação de informações jurídicas brasileiras.", version="1.7.0")
origins = [value.strip() for value in os.getenv("JURISAI_CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",") if value.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-API-Key"])
SYNC_REGISTRY = build_registry()

@app.middleware("http")
async def rate_limit_requests(request: Request, call_next):
    if request.url.path not in {"/health", "/health/details", "/ready"}:
        enforce_rate_limit(request)
    return await call_next(request)

@app.on_event("startup")
def startup() -> None: Base.metadata.create_all(bind=engine)

if os.path.isdir("web"): app.mount("/web", StaticFiles(directory="web", html=True), name="web")

@app.get("/")
def root() -> dict[str, str]: return {"name": "JurisAI-BR", "status": "online", "version": "1.7.0"}

@app.get("/health")
def health() -> dict[str, str]: return {"status": "ok"}

@app.get("/ready")
def ready() -> dict:
    ok, detail = database_ready()
    if not ok: raise HTTPException(status_code=503, detail={"status": "not_ready", "database": detail})
    return {"status": "ready", "database": "ok"}

@app.get("/health/details")
def health_details() -> dict[str, str]: return {"status": "ok", "database": engine.url.get_backend_name()}

@app.get("/v1/sync/status")
def sync_status(actor: str = Depends(require_api_key)) -> dict: return {"sources": SYNC_REGISTRY.names(), "state": load_state()}

@app.post("/v1/sync/{source}")
def sync_source(source: str, actor: str = Depends(require_api_key)) -> dict:
    if source not in SYNC_REGISTRY.names(): raise HTTPException(status_code=404, detail="Fonte não registrada")
    result = SYNC_REGISTRY.execute(source)
    if not result.errors: mark_synced(source, result.finished_at)
    log_event("source_sync", {"actor": actor, "source": source, "imported": result.imported, "skipped": result.skipped, "errors": result.errors})
    return result.__dict__

@app.post("/v1/documents")
def ingest_document(payload: LegalDocumentCreate, session: Session = Depends(get_session), actor: str = Depends(require_api_key)) -> dict:
    document = save_document(session, payload.title, payload.content, payload.source, payload.category)
    log_event("ingest_document", {"actor": actor, "document_id": document.id, "source": payload.source})
    return {"id": document.id, "title": document.title, "category": document.category, "created": True}

@app.post("/v1/documents/upload")
async def upload_document(file: UploadFile = File(...), title: str | None = Form(default=None), source: str | None = Form(default=None), category: str = Form(default="geral"), session: Session = Depends(get_session), actor: str = Depends(require_api_key)) -> dict:
    data = await file.read()
    try: content = extract_text(file.filename or "upload", data)
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc
    if len(content.strip()) < 10: raise HTTPException(status_code=400, detail="Não foi possível extrair conteúdo jurídico suficiente.")
    document = save_document(session, title or file.filename or "Documento", content, source or "upload", category)
    log_event("upload_document", {"actor": actor, "document_id": document.id, "filename": file.filename})
    return {"id": document.id, "title": document.title, "characters": len(content), "created": True}

@app.post("/v1/documents/seed")
def seed_documents(session: Session = Depends(get_session), actor: str = Depends(require_api_key)) -> dict:
    count = seed_demo_data(session); log_event("seed_documents", {"actor": actor, "count": count}); return {"seeded": count}

@app.get("/v1/search")
def search(query: str, session: Session = Depends(get_session), actor: str = Depends(require_api_key)) -> dict:
    results = semantic_document_search(session, query); log_event("search", {"actor": actor, "results": len(results), "mode": "persistent-semantic"}); return {"query": query, "results": results}

@app.post("/v1/classify", response_model=ClassificationResult)
def classify(payload: ClassifyRequest, actor: str = Depends(require_api_key)) -> ClassificationResult:
    area, confidence, keywords = classify_text(payload.text); result = ClassificationResult(area=area, confidence=confidence, matched_keywords=keywords, next_steps=next_steps(area), disclaimer=DISCLAIMER); log_event("classify", {"actor": actor, "area": area, "text_length": len(payload.text)}); return result

@app.post("/v1/analyze-document", response_model=DocumentAnalysisResult)
def analyze(payload: DocumentAnalysisRequest, actor: str = Depends(require_api_key)) -> DocumentAnalysisResult:
    result = DocumentAnalysisResult(**analyze_document(payload.text)); log_event("analyze_document", {"actor": actor, "area": result.area, "text_length": len(payload.text)}); return result

@app.post("/v1/legal-query", response_model=LegalQueryResult)
def legal_query(payload: LegalQueryRequest, actor: str = Depends(require_api_key)) -> LegalQueryResult:
    result = LegalQueryResult(**answer_question(payload.question, payload.context)); log_event("legal_query", {"actor": actor, "area": result.area}); return result

@app.post("/v1/legal-research")
def legal_research(payload: LegalQueryRequest, actor: str = Depends(require_api_key)) -> dict:
    result = answer_with_sources(payload.question, payload.context); log_event("legal_research", {"actor": actor, "area": result["area"], "sources": len(result["sources"]), "grounded": result["grounded"]}); return result

@app.get("/v1/sources")
def sources() -> dict: return list_official_sources()
