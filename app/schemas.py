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
