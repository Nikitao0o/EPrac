from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# экземпляр приложения FastAPI
app = FastAPI(
    title="Intelligent Search API",
    description="API для интеллектуальной поисковой системы по внутренней базе знаний",
    version="1.0.0",
    docs_url="/docs", # Swagger UI будет здесь
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене тут должны быть конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# тестовый эндпоинт, чтобы проверить, что всё работает
@app.get("/api/v1/healthcheck", tags=["System"])
async def healthcheck():
    return {"status": "ok", "message": "Backend is running!"}