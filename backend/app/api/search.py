from fastapi import APIRouter, Query, HTTPException, status
from app.services.es_client import search_chunks

router = APIRouter()


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_documents(q: str = Query(..., description="Поисковый запрос")):
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поисковый запрос не может быть пустым."
        )

    return await search_chunks(query=q)