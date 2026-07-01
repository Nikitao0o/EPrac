import io
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> list[dict]:
    pages_data = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                # сохраняем текст и номер страницы (начинаем с 1)
                pages_data.append({"page_number": i + 1, "text": text.strip()})
    return pages_data


def extract_text_from_docx(file_bytes: bytes) -> list[dict]:
    doc = Document(io.BytesIO(file_bytes))
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())

    combined_text = "\n".join(full_text)
    if not combined_text:
        return []

    return [{"page_number": 1, "text": combined_text}]


def chunk_text(pages_data: list[dict], chunk_size: int = 1000, overlap: int = 100) -> list[dict]:
    chunks = []

    for data in pages_data:
        text = data["text"]
        page_num = data["page_number"]

        if len(text) <= chunk_size:
            chunks.append({
                "page_number": page_num,
                "text": text
            })
            continue

        # нарезка по 1000 символов с нахлестом 100
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_str = text[start:end]
            chunks.append({
                "page_number": page_num,
                "text": chunk_str
            })
            start += chunk_size - overlap

    return chunks