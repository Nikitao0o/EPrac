from fastapi import APIRouter, status
from app.services.es_client import get_uploaded_documents

router = APIRouter()

@router.get("/documents", status_code=status.HTTP_200_OK)
async def get_documents_list():
    return await get_uploaded_documents()