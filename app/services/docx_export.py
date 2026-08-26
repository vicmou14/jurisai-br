from __future__ import annotations

from io import BytesIO
import re
from uuid import uuid4

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

from app.services.template_registry import template_for_profile


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", value).strip("_")
    return cleaned or f"peca_{uuid4().hex[:8]}"


def _clear_body(document: Document) -> None:
    body = document._element.body
    for child in list(body):
        if child.tag.endswith("sectPr"):
            continue
        body.remove(child)


def _configure(document: Document) -> None:
    style = document.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(0)


def _add_content(document: Document, title: str, content: str) -> None:
    heading = document.add_paragraph()
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = heading.add_run(title.upper())
    run.bold = True
    run.font.size = Pt(12)

    for block in [item.strip() for item in content.split("\n\n") if item.strip()]:
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.first_line_indent = Cm(1.25)
        for index, line in enumerate(block.splitlines()):
            run = paragraph.add_run(line)
            if index < len(block.splitlines()) - 1:
                run.add_break()


def export_docx(title: str, content: str, profile: str = "office") -> tuple[str, bytes]:
    document = Document(str(template_for_profile(profile)))
    _clear_body(document)
    _configure(document)
    _add_content(document, title, content)
    output = BytesIO()
    document.save(output)
    return _safe_filename(title) + ".docx", output.getvalue()
