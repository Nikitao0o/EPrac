from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

# Импорт всех роутеров
from app.api.upload import router as upload_router
from app.api.search import router as search_router
from app.api.documents import router as documents_router
from app.services.es_client import create_index_if_not_exists, es


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Логика при старте сервера
    await create_index_if_not_exists()
    yield
    # Логика при остановке сервера
    await es.close()


app = FastAPI(
    title="Intelligent Search API",
    description="API для интеллектуальной поисковой системы по внутренней базе знаний",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(upload_router, prefix="/api/v1", tags=["Documents"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents"])
app.include_router(search_router, prefix="/api/v1", tags=["Search"])

# Prometheus метрики
Instrumentator().instrument(app).expose(app, include_in_schema=False)

@app.get("/api/v1/healthcheck", tags=["System"])
async def healthcheck():
    return {"status": "ok", "message": "Backend is running!"}