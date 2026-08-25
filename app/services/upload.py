from __future__ import annotations

from io import BytesIO


def extract_text(filename: str, data: bytes) -> str:
    name = filename.lower()
    if name.endswith('.txt'):
        return data.decode('utf-8', errors='replace')
    if name.endswith('.pdf'):
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(data))
        return '\n'.join((page.extract_text() or '') for page in reader.pages).strip()
    if name.endswith('.docx'):
        from docx import Document
        document = Document(BytesIO(data))
        return '\n'.join(paragraph.text for paragraph in document.paragraphs).strip()
    raise ValueError('Formato não suportado. Use PDF, DOCX ou TXT.')
