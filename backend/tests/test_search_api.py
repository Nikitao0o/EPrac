from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import search as search_module


app = FastAPI()
app.include_router(search_module.router, prefix="/api/v1")
client = TestClient(app)


def test_search_accepts_frontend_pagination_contract(monkeypatch):
    captured = {}

    async def fake_search_chunks(query, file_name=None, limit=10, offset=0):
        captured.update(
            {
                "query": query,
                "file_name": file_name,
                "limit": limit,
                "offset": offset,
            }
        )
        return {
            "total": 21,
            "items": [
                {
                    "chunk_id": "chunk-1",
                    "file_name": "lecture.pdf",
                    "page": 2,
                    "text": "FastAPI search result",
                    "score": 1.5,
                }
            ],
        }

    monkeypatch.setattr(search_module, "search_chunks", fake_search_chunks)

    response = client.get("/api/v1/search?q=fastapi&page=2&page_size=10")

    assert response.status_code == 200
    assert captured == {
        "query": "fastapi",
        "file_name": None,
        "limit": 10,
        "offset": 10,
    }

    body = response.json()
    assert body["total"] == 21
    assert body["total_results"] == 21
    assert body["page"] == 2
    assert body["page_size"] == 10
    assert body["limit"] == 10
    assert body["offset"] == 10
    assert body["results"][0]["chunk_id"] == "chunk-1"


def test_search_accepts_limit_offset_contract(monkeypatch):
    captured = {}

    async def fake_search_chunks(query, file_name=None, limit=10, offset=0):
        captured.update(
            {
                "query": query,
                "file_name": file_name,
                "limit": limit,
                "offset": offset,
            }
        )
        return {"total": 0, "items": []}

    monkeypatch.setattr(search_module, "search_chunks", fake_search_chunks)

    response = client.get(
        "/api/v1/search?q=elastic&file_name=lecture.pdf&limit=5&offset=15"
    )

    assert response.status_code == 200
    assert captured == {
        "query": "elastic",
        "file_name": "lecture.pdf",
        "limit": 5,
        "offset": 15,
    }

    body = response.json()
    assert body["page"] == 4
    assert body["page_size"] == 5
    assert body["total"] == 0
    assert body["total_results"] == 0
    assert body["results"] == []


def test_search_rejects_blank_query():
    response = client.get("/api/v1/search?q=%20%20")

    assert response.status_code == 400
    assert "не может быть пустым" in response.json()["detail"]
