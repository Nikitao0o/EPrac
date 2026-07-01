import { useCallback, useState } from 'react'
import { uploadDocumentWithProgress } from '../api/client'
import { FileDropzone } from '../components/FileDropzone'
import { UploadQueue } from '../components/UploadQueue'
import type { UploadItem } from '../types/api'
import { validateUploadFile } from '../utils/files'

function createLocalId(): string {
  return crypto.randomUUID()
}

export function UploadPage() {
  const [items, setItems] = useState<UploadItem[]>([])
  const [isBusy, setIsBusy] = useState(false)

  const updateItem = useCallback((localId: string, patch: Partial<UploadItem>) => {
    setItems((current) =>
      current.map((item) => (item.localId === localId ? { ...item, ...patch } : item)),
    )
  }, [])

  const processFile = useCallback(
    async (item: UploadItem) => {
      const validationError = validateUploadFile(item.file)
      if (validationError) {
        updateItem(item.localId, { status: 'error', error: validationError })
        return
      }

      updateItem(item.localId, { status: 'uploading', progress: 0, error: undefined })

      try {
        const response = await uploadDocumentWithProgress(item.file, (progress) => {
          updateItem(item.localId, { progress })
        })

        updateItem(item.localId, { status: 'indexing', progress: 100 })

        await new Promise((resolve) => window.setTimeout(resolve, 400))

        updateItem(item.localId, {
          status: 'ready',
          progress: 100,
          documentId: response.document_id,
          uploadedAt: new Date(),
        })
      } catch (error) {
        updateItem(item.localId, {
          status: 'error',
          error: error instanceof Error ? error.message : 'Не удалось загрузить файл',
        })
      }
    },
    [updateItem],
  )

  const handleFilesSelected = async (files: File[]) => {
    if (files.length === 0) {
      return
    }

    const newItems: UploadItem[] = files.map((file) => ({
      localId: createLocalId(),
      file,
      status: 'pending',
      progress: 0,
    }))

    setItems((current) => [...newItems, ...current])
    setIsBusy(true)

    for (const item of newItems) {
      await processFile(item)
    }

    setIsBusy(false)
  }

  return (
    <>
      <section className="panel">
        <div className="panel__header">
          <div>
            <h2>Загрузка документов</h2>
            <p className="panel__hint">
              Отправка на <code>POST /api/v1/documents/upload</code>. Поддерживаются PDF и DOCX до 20 МБ.
            </p>
          </div>
        </div>
        <FileDropzone onFilesSelected={handleFilesSelected} disabled={isBusy} />
      </section>

      <section className="panel">
        <h2>Загруженные документы</h2>
        <UploadQueue items={items} />
      </section>
    </>
  )
}
