from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.services.es_client import create_index_if_not_exists, es


# функция выполняется при старте и остановке сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    # логика при старте сервера
    await create_index_if_not_exists()

    yield  # сервер работает

    # логика при остановке сервера (закрываем соединение с бд)
    await es.close()


# создаем экземпляр приложения FastAPI и передаем ему lifespan
app = FastAPI(
    title="Intelligent Search API",
    description="API для интеллектуальной поисковой системы по внутренней базе знаний",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключаем роутер
app.include_router(upload_router, prefix="/api/v1", tags=["Documents"])


# тестовый эндпоинт
@app.get("/api/v1/healthcheck", tags=["System"])
async def healthcheck():
    return {"status": "ok", "message": "Backend is running!"}