from app.services.parser import chunk_text


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
