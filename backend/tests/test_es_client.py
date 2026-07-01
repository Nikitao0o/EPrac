import pytest

from app.services import es_client


@pytest.fixture
def anyio_backend():
    return "asyncio"


class FakeElasticsearch:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def search(self, index, body):
        self.calls.append({"index": index, "body": body})
        return self.response


@pytest.mark.anyio
async def test_index_chunks_sends_bulk_actions(monkeypatch):
    captured = {}

    async def fake_async_bulk(client, actions):
        captured["client"] = client
        captured["actions"] = actions

    fake_es = object()
    monkeypatch.setattr(es_client, "es", fake_es)
    monkeypatch.setattr(es_client, "async_bulk", fake_async_bulk)

    await es_client.index_chunks(
        [{"page_number": 2, "text": "indexed chunk"}],
        "lecture.pdf",
    )

    assert captured["client"] is fake_es
    assert len(captured["actions"]) == 1
    action = captured["actions"][0]
    assert action["_index"] == "documents"
    assert action["_source"]["file_name"] == "lecture.pdf"
    assert action["_source"]["page_number"] == 2
    assert action["_source"]["text"] == "indexed chunk"


@pytest.mark.anyio
async def test_search_chunks_builds_filtered_query_and_maps_hits(monkeypatch):
    fake_es = FakeElasticsearch(
        {
            "hits": {
                "total": {"value": 1},
                "hits": [
                    {
                        "_score": 2.5,
                        "_source": {
                            "chunk_id": "chunk-1",
                            "file_name": "lecture.pdf",
                            "page_number": 4,
                            "text": "FastAPI and Elasticsearch",
                        },
                    }
                ],
            }
        }
    )
    monkeypatch.setattr(es_client, "es", fake_es)

    result = await es_client.search_chunks(
        "fastapi",
        file_name="lecture.pdf",
        limit=5,
        offset=10,
    )

    call = fake_es.calls[0]
    assert call["index"] == "documents"
    assert call["body"]["from"] == 10
    assert call["body"]["size"] == 5
    assert call["body"]["query"]["bool"]["filter"] == [
        {"term": {"file_name": "lecture.pdf"}}
    ]
    assert result == {
        "total": 1,
        "items": [
            {
                "chunk_id": "chunk-1",
                "file_name": "lecture.pdf",
                "page": 4,
                "text": "FastAPI and Elasticsearch",
                "score": 2.5,
            }
        ],
    }


@pytest.mark.anyio
async def test_get_uploaded_documents_maps_aggregation(monkeypatch):
    fake_es = FakeElasticsearch(
        {
            "aggregations": {
                "unique_files": {
                    "buckets": [
                        {"key": "lecture-01.pdf", "doc_count": 3},
                        {"key": "lecture-02.pdf", "doc_count": 7},
                    ]
                }
            }
        }
    )
    monkeypatch.setattr(es_client, "es", fake_es)

    result = await es_client.get_uploaded_documents()

    assert fake_es.calls[0]["body"]["size"] == 0
    assert result == [
        {"file_name": "lecture-01.pdf", "chunks_count": 3},
        {"file_name": "lecture-02.pdf", "chunks_count": 7},
    ]
