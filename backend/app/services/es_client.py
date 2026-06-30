import uuid
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from app.core.config import ELASTICSEARCH_URL

# асинхронный клиент для работы с базой
es = AsyncElasticsearch(ELASTICSEARCH_URL)

INDEX_NAME = "documents"


async def create_index_if_not_exists():
    # описание структуры индекса (Требование BE-06)
    mapping = {
        "mappings": {
            "properties": {
                "chunk_id": {"type": "keyword"},
                "file_name": {"type": "keyword"},
                "page_number": {"type": "integer"},
                "text": {
                    "type": "text",
                    "analyzer": "russian"
                }
            }
        }
    }

    try:
        exists = await es.indices.exists(index=INDEX_NAME)
        if not exists:
            await es.indices.create(index=INDEX_NAME, body=mapping)
            print(f"Индекс '{INDEX_NAME}' успешно создан.")
        else:
            print(f"Индекс '{INDEX_NAME}' уже существует.")
    except Exception as e:
        print(f"ВНИМАНИЕ: Не удалось подключиться к Elasticsearch. Ошибка: {e}")


async def index_chunks(chunks: list[dict], file_name: str) -> None:
    # массовая загрузка чанков в Elasticsearch
    actions = []
    for chunk in chunks:
        action = {
            "_index": INDEX_NAME,
            "_id": str(uuid.uuid4()),
            "_source": {
                "chunk_id": str(uuid.uuid4()),
                "file_name": file_name,
                "page_number": chunk["page_number"],
                "text": chunk["text"]
            }
        }
        actions.append(action)

    try:
        await async_bulk(es, actions)
    except Exception as e:
        print(f"Ошибка при индексации в Elasticsearch: {e}")
        raise e


async def search_chunks(query: str, file_name: str = None, limit: int = 10) -> list[dict]:
    # полнотекстовый поиск по чанкам с оптимизацией через фильтры

    # базовая структура запроса с полнотекстовым поиском multi_match
    search_query = {
        "multi_match": {
            "query": query,
            "fields": ["text", "file_name"]
        }
    }

    # если передан file_name, оборачиваем наш запрос в bool/filter для оптимизации
    if file_name:
        body_query = {
            "bool": {
                "must": search_query,
                "filter": [
                    {"term": {"file_name": file_name}}
                ]
            }
        }
    else:
        body_query = search_query

    body = {
        "size": limit,
        "query": body_query
    }

    try:
        response = await es.search(index=INDEX_NAME, body=body)
        results = []

        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append({
                "chunk_id": source.get("chunk_id"),
                "file_name": source.get("file_name"),
                "page": source.get("page_number"),
                "text": source.get("text"),
                "score": hit["_score"]
            })

        return results
    except Exception as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return []


async def get_uploaded_documents() -> list[dict]:
    # получение списка уникальных загруженных файлов через агрегацию
    body = {
        "size": 0,
        "aggs": {
            "unique_files": {
                "terms": {"field": "file_name", "size": 1000}
            }
        }
    }

    try:
        response = await es.search(index=INDEX_NAME, body=body)
        buckets = response["aggregations"]["unique_files"]["buckets"]

        documents = []
        for bucket in buckets:
            documents.append({
                "file_name": bucket["key"],
                "chunks_count": bucket["doc_count"]
            })

        return documents
    except Exception as e:
        print(f"Ошибка при получении списка документов: {e}")
        return []