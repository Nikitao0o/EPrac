import os


# Базовый URL для подключения к Elasticsearch.
# В docker-compose переопределяется на http://elasticsearch:9200.
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
