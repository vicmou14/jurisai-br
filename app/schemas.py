from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

LegalArea = Literal[
    "civil", "consumidor", "trabalhista", "familia", "criminal",
    "tributario", "previdenciario", "administrativo", "empresarial", "desconhecida",
]

class ClassifyRequest(BaseModel):
    text: str = Field(min_length=10, max_length=20000)

class DocumentAnalysisRequest(BaseModel):
    text: str = Field(min_length=20, max_length=50000)

class LegalQueryRequest(BaseModel):
    question: str = Field(min_length=10, max_length=20000)
    context: str | None = Field(default=None, max_length=20000)

class DraftPrepareRequest(BaseModel):
    instruction: str = Field(min_length=5, max_length=50000)
    context: str | None = Field(default=None, max_length=100000)

class DraftDocumentInput(BaseModel):
    title: str = Field(default="Documento", min_length=1, max_length=500)
    content: str = Field(min_length=1, max_length=200000)

class DraftGenerateRequest(DraftPrepareRequest):
    documents: list[DraftDocumentInput] = Field(default_factory=list, max_length=20)

class DraftExportRequest(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    content: str = Field(min_length=1, max_length=500000)
    profile: Literal["coder", "office"] = "office"

class LegalDocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    content: str = Field(min_length=10, max_length=200000)
    source: str = Field(min_length=3, max_length=1000)
    category: str = Field(default="geral", max_length=100)

class ClassificationResult(BaseModel):
    area: LegalArea
    confidence: float = Field(ge=0, le=1)
    matched_keywords: list[str]
    next_steps: list[str]
    disclaimer: str

class DocumentAnalysisResult(BaseModel):
    area: LegalArea
    confidence: float = Field(ge=0, le=1)
    summary: str
    parties: list[str]
    dates: list[str]
    values: list[str]
    risks: list[str]
    disclaimer: str

class LegalQueryResult(BaseModel):
    area: LegalArea
    confidence: float = Field(ge=0, le=1)
    answer: str
    suggested_documents: list[str]
    disclaimer: str
