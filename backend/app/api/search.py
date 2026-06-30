from fastapi import APIRouter, Query, HTTPException, status
from app.services.es_client import search_chunks

router = APIRouter()


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_documents(
    q: str = Query(..., description="Поисковый запрос"),
    file_name: str = Query(None, description="Фильтр по конкретному имени файла"),
    limit: int = Query(10, ge=1, le=100, description="Количество результатов")
):
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поисковый запрос не может быть пустым."
        )

    try:
        # передаем параметры в оптимизированный поиск
        results = await search_chunks(query=q, file_name=file_name, limit=limit)
        return {
            "query": q,
            "filter_file_name": file_name,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка на сервере при поиске: {str(e)}"
        )