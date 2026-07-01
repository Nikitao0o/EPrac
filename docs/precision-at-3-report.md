# Отчёт Precision@3

## Цель

Проверить качество поисковой выдачи на 10 эталонных запросах.
Запрос считается успешным, если ожидаемый документ попал в топ-3 результатов.

## Результаты

| Запрос | Ожидаемый документ | Топ-3 | Попал в топ-3 |
| --- | --- | --- | --- |
| FastAPI Swagger | `qa-fastapi-openapi.docx` | qa-fastapi-openapi.docx | да |
| Elasticsearch analyzer | `qa-elasticsearch-analyzer.docx` | qa-elasticsearch-analyzer.docx, qa-docker-compose-monitoring.docx | да |
| Docker Compose services | `qa-docker-compose-monitoring.docx` | qa-docker-compose-monitoring.docx | да |
| Redis TTL cache | `qa-redis-cache-ttl.docx` | qa-redis-cache-ttl.docx, qa-docker-compose-monitoring.docx | да |
| React Vite frontend | `qa-react-vite-frontend.docx` | qa-react-vite-frontend.docx, qa-docker-compose-monitoring.docx | да |
| PDF DOCX parser | `qa-parser-pdf-docx.docx` | qa-parser-pdf-docx.docx, valid-lecture.docx | да |
| chunk overlap metadata | `qa-chunk-overlap-index.docx` | qa-chunk-overlap-index.docx | да |
| Prometheus Grafana metrics | `qa-prometheus-grafana.docx` | qa-prometheus-grafana.docx, qa-docker-compose-monitoring.docx | да |
| Precision top results | `qa-precision-evaluation.docx` | qa-precision-evaluation.docx, qa-playwright-e2e.docx | да |
| Playwright E2E scenario | `qa-playwright-e2e.docx` | qa-playwright-e2e.docx | да |

## Итог

Precision@3: 1.00

Успешных запросов: 10 из 10.
