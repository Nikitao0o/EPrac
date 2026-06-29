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
| BE-01 | `POST /api/v1/documents/upload` | Готово | Реализован эндпоинт загрузки одного файла. |
| BE-02 | Валидация: PDF/DOCX, ≤20 МБ, иначе 400 | Готово | Проверяются расширение, content-type и размер. |
| BE-03 | Генерация UUID для документа | Готово | UUID возвращается в ответе upload endpoint. |
| BE-04 | Извлечение текста (pdfplumber, python-docx) | Не начато | Парсеры документов пока не добавлены. |
| BE-05 | Чанкинг: 1000 символов, overlap 100 | Не начато | Сервис чанкинга пока не добавлен. |
| BE-06 | Elasticsearch с analysis-ru, индекс `documents` | Частично | Клиент и индекс `documents` с analyzer `russian` создаются при старте. |
| BE-07 | Индексация чанков с метаданными | Не начато | Индексация загруженных документов пока не реализована. |
| BE-08 | `GET /api/v1/search?q={query}` multi-match | Не начато | Поисковый эндпоинт пока не добавлен. |
| BE-09 | Ответ JSON: chunk_id, file_name, page, text, score | Не начато | Будет реализовано вместе с поиском. |
| API-01 | OpenAPI 3.0, Swagger UI по `/docs` | Готово | FastAPI публикует Swagger UI по `/docs`. |
| API-02 | Статусы: 200, 400, 404, 500 | Частично | 200/400 есть в загрузке; остальные нужны в следующих эндпоинтах. |
| FE-01 | Drag-and-Drop, множественная загрузка | Не начато | Frontend-приложение пока не создано. |
| FE-02 | Прогресс-бары загрузки/индексации | Не начато | Frontend-приложение пока не создано. |
| FE-03 | Список загруженных документов | Не начато | Нужны frontend и backend endpoint списка документов. |
| FE-04 | Поле ввода + кнопка «Найти» | Не начато | Frontend-приложение пока не создано. |
| FE-05 | Карточки результатов поиска | Не начато | Зависит от search endpoint. |
| FE-06 | Подсветка совпадений | Не начато | Зависит от frontend поиска. |
| FE-07 | Пагинация или бесконечный скролл | Не начато | Зависит от frontend поиска. |
| FE-08 | Сообщение при пустом результате | Не начато | Зависит от frontend поиска. |
| FE-09 | Адаптивная вёрстка 320–1920px | Не начато | Frontend-приложение пока не создано. |
| DO-01 | Dockerfile для бэкенда | Готово | Добавлен `backend/Dockerfile`. |
| DO-02 | Dockerfile для фронтенда | Частично | Добавлен Node -> Nginx Dockerfile с временной HTML-заглушкой до появления React/Vite. |
| DO-03 | `docker-compose.yml`: app, front, postgres, elasticsearch, redis | Готово | Все требуемые сервисы добавлены; также подключены Prometheus и Grafana. |
| DO-04 | `.env` + `.env.example` для секретов | Готово | `.env.example` в репозитории, `.env` игнорируется git. |
| DO-05 | GitHub Actions: линтеры, тесты, сборка на push в main | Готово | Добавлен workflow для backend lint/test/build, frontend image build и compose validation. |
| DO-06 | Prometheus + Grafana | Частично | Сервисы и `/metrics` добавлены; отдельные метрики `/search` появятся после поискового эндпоинта. |
| DO-07 | `init.sh` для скачивания и загрузки 10 PDF-лекций | Не начато | Скрипт пока не добавлен. |
| QA-01 | Юнит-тесты pytest, покрытие ≥50% | Частично | Добавлены тесты валидации эндпоинта загрузки; порог покрытия 50% выполняется. Тесты парсинга появятся после реализации парсеров. |
| QA-02 | E2E Playwright: загрузка → индексация → поиск → вывод | Не начато | Зависит от frontend и полного backend flow. |
| QA-03 | Набор тестовых документов | Готово | Фикстуры добавлены в `backend/tests/fixtures`: валидные, пустые, битые и неподдерживаемые файлы. |
| QA-04 | Нагрузочные тесты на 50 пользователей | Не начато | Нагрузочный сценарий и отчёт пока не добавлены. |
| QA-05 | Precision@3 для 10 запросов | Не начато | Оценочный набор пока не добавлен. |
| QA-06 | Руководство пользователя | Частично | Добавлено текущее руководство для доступного API загрузки; финальная версия зависит от frontend и поиска. |

## Git Workflow

Рабочая DevOps-ветка: `emin/devops`.

Базовый порядок работы:

```bash
git switch emin/devops
git pull
# внести изменения
git add .
git commit -m "feat: короткое описание"
git push
```

После проверки изменения мержатся в `main` через Pull Request.
