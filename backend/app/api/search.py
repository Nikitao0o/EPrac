from fastapi import APIRouter, Query, HTTPException, status
from app.services.es_client import search_chunks

router = APIRouter()


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_documents(
        q: str = Query(..., description="Поисковый запрос"),
        file_name: str = Query(None, description="Фильтр по конкретному имени файла"),
        page: int = Query(1, ge=1, description="Номер страницы для фронтенда"),
        page_size: int = Query(10, ge=1, le=100, description="Размер страницы для фронтенда"),
        limit: int | None = Query(None, ge=1, le=100, description="Количество результатов на страницу"),
        offset: int | None = Query(None, ge=0, description="Смещение от начала результатов")
):
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поисковый запрос не может быть пустым."
        )

    try:
        # Поддерживаем оба контракта пагинации: page/page_size для фронта и limit/offset для API.
        effective_limit = limit if limit is not None else page_size
        effective_offset = offset if offset is not None else (page - 1) * effective_limit
        effective_page = (effective_offset // effective_limit) + 1

        search_result = await search_chunks(
            query=q,
            file_name=file_name,
            limit=effective_limit,
            offset=effective_offset,
        )
        total = search_result["total"]

        return {
            "query": q,
            "filter_file_name": file_name,
            "total": total,
            "total_results": total,
            "page": effective_page,
            "page_size": effective_limit,
            "limit": effective_limit,
            "offset": effective_offset,
            "results": search_result["items"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка на сервере при поиске: {str(e)}"
        )
