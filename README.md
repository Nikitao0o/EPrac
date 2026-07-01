# EPrac

EPrac — учебный проект полнотекстового поискового веб-приложения по документам. Цель проекта: загрузка PDF/DOCX, извлечение и индексация текста, поиск по базе документов через FastAPI и Elasticsearch, а также полноценное окружение для разработки, тестирования и мониторинга.

Полное техническое задание хранится в [docs/technical-spec.md](docs/technical-spec.md).

## Стек

- **Backend:** Python, FastAPI, Elasticsearch, PostgreSQL, Redis
- **Frontend:** TypeScript, React/Vite, Nginx
- **DevOps:** Docker, Docker Compose, GitHub Actions, Prometheus, Grafana
- **Testing:** Pytest, Playwright

## Быстрый старт

1. Скопировать переменные окружения:

```bash
cp .env.example .env
```

2. Запустить стек:

```bash
docker compose up --build
```

3. Основные адреса:

| Сервис | URL |
|--------|-----|
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Frontend | http://localhost:8080 |
| Elasticsearch | http://localhost:9200 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## Текущий статус

| ID | Требование | Статус | Комментарий |
|----|------------|--------|-------------|
| BE-01 | `POST /api/v1/documents/upload` | Готово | Эндпоинт принимает PDF/DOCX, запускает парсинг, чанкинг и индексацию. |
| BE-02 | Валидация: PDF/DOCX, ≤20 МБ, иначе 400 | Готово | Проверяются расширение, content-type, размер и наличие извлеченного текста. |
| BE-03 | Генерация UUID для документа | Готово | UUID возвращается в ответе upload endpoint. |
| BE-04 | Извлечение текста (pdfplumber, python-docx) | Готово | Добавлены парсеры PDF и DOCX в `backend/app/services/parser.py`. |
| BE-05 | Чанкинг: 1000 символов, overlap 100 | Готово | Реализован `chunk_text` с размером 1000 и overlap 100. |
| BE-06 | Elasticsearch с analysis-ru, индекс `documents` | Частично | Индекс `documents` создается при старте с русским analyzer; стоит отдельно проверить требование именно `analysis-ru`. |
| BE-07 | Индексация чанков с метаданными | Готово | Чанки индексируются с `chunk_id`, `file_name`, `page_number`, `text`. |
| BE-08 | `GET /api/v1/search?q={query}` multi-match | Готово | Поиск реализован через Elasticsearch `multi_match`, есть фильтр `file_name`. |
| BE-09 | Ответ JSON: chunk_id, file_name, page, text, score | Готово | Ответ содержит `results`; также поддержаны `total` и `total_results` для фронта. |
| API-01 | OpenAPI 3.0, Swagger UI по `/docs` | Готово | FastAPI публикует Swagger UI по `/docs`. |
| API-02 | Статусы: 200, 400, 404, 500 | Частично | Основные 200/400/500 обработаны; 404 нужно проверить после финализации API. |
| FE-01 | Drag-and-Drop, множественная загрузка | Готово | Реализован `FileDropzone`, поддержан выбор нескольких файлов. |
| FE-02 | Прогресс-бары загрузки/индексации | Готово | Очередь загрузки показывает статусы `uploading`, `indexing`, `ready`, `error`. |
| FE-03 | Список загруженных документов | Частично | Есть локальный список загруженных файлов; backend `GET /api/v1/documents` есть, но фронт пока не синхронизирует список с сервером. |
| FE-04 | Поле ввода + кнопка «Найти» | Готово | Поиск запускается кнопкой и Enter. |
| FE-05 | Карточки результатов поиска | Готово | Карточки показывают файл, страницу, фрагмент и score. |
| FE-06 | Подсветка совпадений | Готово | Совпадения подсвечиваются компонентом `HighlightedText`. |
| FE-07 | Пагинация или бесконечный скролл | Готово | Реализована пагинация по 10 результатов. |
| FE-08 | Сообщение при пустом результате | Готово | Пустой результат отображается отдельным состоянием. |
| FE-09 | Адаптивная вёрстка 320–1920px | Частично | Базовая адаптивность есть; нужна ручная QA-проверка на 320, 768, 1440, 1920px. |
| DO-01 | Dockerfile для бэкенда | Готово | Добавлен `backend/Dockerfile`. |
| DO-02 | Dockerfile для фронтенда | Готово | Добавлен Node -> Nginx Dockerfile для React/Vite приложения. |
| DO-03 | `docker-compose.yml`: app, front, postgres, elasticsearch, redis | Готово | Все требуемые сервисы добавлены; также подключены Prometheus и Grafana. |
| DO-04 | `.env` + `.env.example` для секретов | Готово | `.env.example` в репозитории, `.env` игнорируется git. |
| DO-05 | GitHub Actions: линтеры, тесты, сборка на push в main | Готово | Добавлен workflow для backend lint/test/build, frontend image build и compose validation. |
| DO-06 | Prometheus + Grafana | Частично | Сервисы и `/metrics` добавлены; нужно настроить dashboard и проверить метрики `/search`. |
| DO-07 | `init.sh` для скачивания и загрузки 10 PDF-лекций | Не начато | Скрипт пока не добавлен. |
| QA-01 | Юнит-тесты pytest, покрытие ≥50% | Готово | CI запускает pytest с порогом покрытия 50%; добавлены тесты upload/search/parser/es_client. |
| QA-02 | E2E Playwright: загрузка → индексация → поиск → вывод | Не начато | Зависит от frontend и полного backend flow. |
| QA-03 | Набор тестовых документов | Готово | Фикстуры добавлены в `backend/tests/fixtures`: валидные, пустые, битые и неподдерживаемые файлы. |
| QA-04 | Нагрузочные тесты на 50 пользователей | Не начато | Нагрузочный сценарий и отчёт пока не добавлены. |
| QA-05 | Precision@3 для 10 запросов | Не начато | Оценочный набор пока не добавлен. |
| QA-06 | Руководство пользователя | Частично | Руководство обновлено под доступные API загрузки, поиска и списка документов; финальную версию стоит дополнить после полной ручной проверки. |

## План дальше

### Ближайший приоритет

1. Интеграционно проверить полный flow в Docker Compose: загрузка PDF/DOCX → индексация → поиск во фронте.
2. Отключить mock-поиск на фронте через `VITE_SEARCH_MOCK=false` и убедиться, что фронт работает с реальным `GET /api/v1/search`.
3. Подключить frontend-список документов к `GET /api/v1/documents`, чтобы список не жил только в локальном состоянии страницы.
4. Проверить Elasticsearch analyzer: подтвердить, что текущий `russian` analyzer закрывает требование `analysis-ru`, либо добавить явные настройки индекса.
5. Доделать DevOps-низкий/средний приоритет: Grafana dashboard и `init.sh` для загрузки 10 PDF-лекций.
6. Закрыть QA-блок: Playwright E2E, нагрузочный тест на 50 пользователей, Precision@3 и финальную версию руководства пользователя.

### По ролям

| Роль | Что делать дальше |
|------|-------------------|
| Backend | Проверить upload/search на реальных файлах, уточнить analyzer Elasticsearch, при необходимости добавить хранение документов в PostgreSQL. |
| Frontend | Переключить поиск с mock на backend, подключить серверный список документов, проверить адаптивность и ошибки API. |
| DevOps | Проверить `docker compose up --build` на чистом окружении, подготовить Grafana dashboard, добавить `init.sh`, следить за CI. |
| QA | Написать Playwright E2E, подготовить отчет по нагрузке, сделать Precision@3 таблицу и обновить руководство пользователя после ручной проверки. |

## Git Workflow

Актуальная версия проекта находится в `main`. Перед продолжением работы каждый участник должен подтянуть `main` в свою ветку:

```bash
git fetch origin
git switch <your-branch>
git merge origin/main
```

Новые задачи лучше начинать от свежего `main`:

```bash
git fetch origin
git switch main
git pull origin main
git switch -c feature/<task-name>
```

После изменений:

```bash
git add .
git commit -m "feat: короткое описание"
git push
```

После проверки изменения мержатся в `main` через Pull Request.
