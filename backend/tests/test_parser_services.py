from pathlib import Path

from app.services.parser import chunk_text, extract_text_from_docx, extract_text_from_pdf


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_chunk_text_keeps_short_page_as_single_chunk():
    chunks = chunk_text([{"page_number": 3, "text": "short lecture text"}])

    assert chunks == [{"page_number": 3, "text": "short lecture text"}]


def test_chunk_text_splits_long_page_with_overlap():
    chunks = chunk_text(
        [{"page_number": 1, "text": "abcdefghijklmnopqrstuvwxyz"}],
        chunk_size=10,
        overlap=2,
    )

    assert chunks == [
        {"page_number": 1, "text": "abcdefghij"},
        {"page_number": 1, "text": "ijklmnopqr"},
        {"page_number": 1, "text": "qrstuvwxyz"},
        {"page_number": 1, "text": "yz"},
    ]


def test_extract_text_from_pdf_fixture():
    file_bytes = (FIXTURES_DIR / "valid-lecture.pdf").read_bytes()

    pages = extract_text_from_pdf(file_bytes)

    assert pages
    assert pages[0]["page_number"] == 1
    assert pages[0]["text"].strip()


def test_extract_text_from_docx_fixture():
    file_bytes = (FIXTURES_DIR / "valid-lecture.docx").read_bytes()

    pages = extract_text_from_docx(file_bytes)

    assert pages
    assert pages[0]["page_number"] == 1
    assert "EPrac" in pages[0]["text"]
    assert "DOCX" in pages[0]["text"]
    assert "QA" in pages[0]["text"]
