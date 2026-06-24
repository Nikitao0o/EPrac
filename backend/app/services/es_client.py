from elasticsearch import AsyncElasticsearch
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
                    "analyzer": "russian"  # русскоязычный анализатор
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