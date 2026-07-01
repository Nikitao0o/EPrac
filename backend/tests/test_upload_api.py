import re

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import upload as upload_module


app = FastAPI()
app.include_router(upload_module.router, prefix="/api/v1")
client = TestClient(app)


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)


def upload_file(filename: str, content: bytes, content_type: str):
    return client.post(
        "/api/v1/documents/upload",
        files={"file": (filename, content, content_type)},
    )


def stub_successful_processing(monkeypatch):
    monkeypatch.setattr(
        upload_module,
        "extract_text_from_pdf",
        lambda _: [{"page_number": 1, "text": "Тестовая лекция PDF"}],
    )
    monkeypatch.setattr(
        upload_module,
        "extract_text_from_docx",
        lambda _: [{"page_number": 1, "text": "Тестовая лекция DOCX"}],
    )
    monkeypatch.setattr(
        upload_module,
        "chunk_text",
        lambda *_args, **_kwargs: [{"page_number": 1, "text": "Тестовый чанк"}],
    )

    async def fake_index_chunks(_chunks, _filename):
        return None

    monkeypatch.setattr(upload_module, "index_chunks", fake_index_chunks)


def test_upload_valid_pdf_returns_document_metadata(monkeypatch):
    stub_successful_processing(monkeypatch)

    response = upload_file(
        "lecture.pdf",
        b"%PDF-1.4\n% test pdf content\n",
        "application/pdf",
    )

    assert response.status_code == 200
    body = response.json()
    assert UUID_PATTERN.match(body["document_id"])
    assert body["filename"] == "lecture.pdf"
    assert body["size_bytes"] == 28
    assert body["total_chunks_indexed"] == 1


def test_upload_valid_docx_returns_document_metadata(monkeypatch):
    stub_successful_processing(monkeypatch)

    response = upload_file(
        "lecture.docx",
        b"PK\x03\x04 test docx content",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    assert response.status_code == 200
    body = response.json()
    assert UUID_PATTERN.match(body["document_id"])
    assert body["filename"] == "lecture.docx"
    assert body["total_chunks_indexed"] == 1


def test_upload_rejects_unsupported_extension():
    response = upload_file("notes.txt", b"plain text", "text/plain")

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]
    assert "DOCX" in response.json()["detail"]


def test_upload_rejects_mismatched_content_type():
    response = upload_file("lecture.pdf", b"fake pdf", "text/plain")

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]
    assert "DOCX" in response.json()["detail"]


def test_upload_rejects_file_larger_than_limit(monkeypatch):
    monkeypatch.setattr(upload_module, "MAX_FILE_SIZE", 5)

    response = upload_file("large.pdf", b"123456", "application/pdf")

    assert response.status_code == 400
    assert "20" in response.json()["detail"]
