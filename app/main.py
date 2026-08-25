"""Ponto de entrada inicial da API do JurisAI-BR."""

from fastapi import FastAPI

app = FastAPI(
    title="JurisAI-BR",
    description="API inicial para inteligência artificial jurídica brasileira.",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "JurisAI-BR",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
