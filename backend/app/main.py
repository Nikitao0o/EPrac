from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router

# экземпляр приложения FastAPI
app = FastAPI(
    title="Intelligent Search API",
    description="API для интеллектуальной поисковой системы по внутренней базе знаний",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# роутер с эндпоинтом загрузки
# префикс /api/v1 добавится ко всем путям из upload_router
app.include_router(upload_router, prefix="/api/v1", tags=["Documents"])

# тестовый эндпоинт
@app.get("/api/v1/healthcheck", tags=["System"])
async def healthcheck():
    return {"status": "ok", "message": "Backend is running!"}