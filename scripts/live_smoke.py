from __future__ import annotations

import os
from io import BytesIO
from zipfile import ZipFile

from openai import OpenAI

from app.services.docx_export import export_docx


def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY ausente para o teste de integração.")

    model = os.getenv("JURISAI_TEXT_MODEL", "gpt-5.6-sol")
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input="Responda apenas: OK",
        max_output_tokens=32,
    )
    if (response.output_text or "").strip() != "OK":
        raise RuntimeError("Resposta inesperada do modelo no smoke test.")

    for profile in ("office", "coder"):
        filename, data = export_docx(
            title="Teste de integração",
            content="Documento de teste gerado pelo JurisAI-BR.",
            profile=profile,
        )
        if not filename.endswith(".docx"):
            raise RuntimeError(f"Nome de arquivo inválido para o perfil {profile}.")
        with ZipFile(BytesIO(data)) as archive:
            if "word/document.xml" not in archive.namelist():
                raise RuntimeError(f"DOCX inválido para o perfil {profile}.")

    print(f"Live smoke test aprovado para o modelo {model} e os perfis office/coder.")


if __name__ == "__main__":
    main()
