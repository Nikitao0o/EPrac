from fastapi import APIRouter, Query, HTTPException, status
from app.services.es_client import search_chunks

router = APIRouter()


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_documents(
        q: str = Query(..., description="Поисковый запрос"),
        file_name: str = Query(None, description="Фильтр по конкретному имени файла"),
        limit: int = Query(10, ge=1, le=100, description="Количество результатов на страницу"),
        offset: int = Query(0, ge=0, description="Смещение (сколько результатов пропустить с начала)")
):
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поисковый запрос не может быть пустым."
        )

    try:
        # передаем параметры пагинации (limit и offset)
        search_result = await search_chunks(query=q, file_name=file_name, limit=limit, offset=offset)

        return {
            "query": q,
            "filter_file_name": file_name,
            "total_results": search_result["total"],  # число найденных чанков
            "limit": limit,
            "offset": offset,
            "results": search_result["items"]  # карточки с текстом
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка на сервере при поиске: {str(e)}"
        )