import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status

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

    # генерация уникального идентификатора (BE-03)
    document_id = str(uuid.uuid4())

    # возвращаем успешный ответ для проверки
    return {
        "message": "Файл успешно загружен и прошел валидацию",
        "document_id": document_id,
        "filename": filename,
        "size_bytes": file_size
    }