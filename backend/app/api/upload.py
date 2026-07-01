import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.parser import extract_text_from_pdf, extract_text_from_docx, chunk_text
from app.services.es_client import index_chunks

# роутер для группировки эндпоинтов
router = APIRouter()

# константы для валидации
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 МБ в байтах
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}


@router.post("/documents/upload", status_code=status.HTTP_200_OK)
async def upload_document(file: UploadFile = File(...)):
    # валидация формата файла (BE-02)
    filename = file.filename or ""
    ext = "." + filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS or file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недопустимый формат файла. Разрешены только PDF и DOCX."
        )

    # валидация размера файла (BE-02)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Размер файла превышает допустимые 20 МБ."
        )

    # чтение файла в память
    file_bytes = await file.read()

    # парсинг текста в зависимости от расширения (BE-04)
    try:
        if ext == ".pdf":
            pages_data = extract_text_from_pdf(file_bytes)
        elif ext == ".docx":
            pages_data = extract_text_from_docx(file_bytes)
        else:
            pages_data = []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при извлечении текста: {str(e)}"
        )

    if not pages_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось извлечь текст. Возможно, файл пуст или состоит только из картинок."
        )

    # чанкование текста (BE-05)
    chunks = chunk_text(pages_data, chunk_size=1000, overlap=100)

    # индексация в Elasticsearch (BE-07)
    try:
        await index_chunks(chunks, filename)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при сохранении данных в поисковый индекс Elasticsearch."
        )

    # генерация уникального идентификатора для файла (BE-03)
    document_id = str(uuid.uuid4())

    # возвращаем успешный ответ
    return {
        "message": "Файл успешно загружен, распарсен и проиндексирован",
        "document_id": document_id,
        "filename": filename,
        "size_bytes": file_size,
        "total_chunks_indexed": len(chunks)
    }
