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
        # проверяем существует ли уже такой индекс
        exists = await es.indices.exists(index=INDEX_NAME)
        if not exists:
            # если нет, создаем его с нашим маппингом
            await es.indices.create(index=INDEX_NAME, body=mapping)
            print(f"Индекс '{INDEX_NAME}' успешно создан в Elasticsearch!")
        else:
            print(f"Индекс '{INDEX_NAME}' уже существует. Пропускаем создание.")
    except Exception as e:
        print(f"ВНИМАНИЕ: Не удалось подключиться к Elasticsearch. Ошибка: {e}")


async def index_chunks(chunks: list[dict], file_name: str) -> None:
    # функция для массовой загрузки чанков в Elasticsearch
    actions = []
    for chunk in chunks:
        action = {
            "_index": INDEX_NAME,
            "_id": str(uuid.uuid4()),  # уникальный ID для каждого документа в ES
            "_source": {
                "chunk_id": str(uuid.uuid4()),
                "file_name": file_name,
                "page_number": chunk["page_number"],
                "text": chunk["text"]
            }
        }
        actions.append(action)

    try:
        # используем async_bulk для быстрой вставки всех чанков разом
        await async_bulk(es, actions)
    except Exception as e:
        print(f"Ошибка при индексации в Elasticsearch: {e}")
        raise e