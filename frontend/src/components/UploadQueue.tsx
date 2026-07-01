import type { UploadItem } from '../types/api'
import { formatBytes, formatDate } from '../utils/files'

interface UploadQueueProps {
  items: UploadItem[]
}

const STATUS_LABELS: Record<UploadItem['status'], string> = {
  pending: 'В очереди',
  uploading: 'Загрузка',
  indexing: 'Индексация',
  ready: 'Готово',
  error: 'Ошибка',
}

export function UploadQueue({ items }: UploadQueueProps) {
  if (items.length === 0) {
    return (
      <p className="empty-state">Загруженные документы появятся здесь после отправки файлов.</p>
    )
  }

  return (
    <ul className="upload-list">
      {items.map((item) => (
        <li key={item.localId} className="upload-list__item">
          <div className="upload-list__header">
            <div>
              <p className="upload-list__name">{item.file.name}</p>
              <p className="upload-list__meta">
                {formatBytes(item.file.size)}
                {item.uploadedAt ? ` · ${formatDate(item.uploadedAt)}` : ''}
              </p>
            </div>
            <span className={`upload-status upload-status--${item.status}`}>
              {STATUS_LABELS[item.status]}
            </span>
          </div>

          {(item.status === 'uploading' || item.status === 'indexing') && (
            <div className="progress">
              <div
                className="progress__bar"
                style={{ width: `${item.status === 'indexing' ? 100 : item.progress}%` }}
              />
            </div>
          )}

          {item.status === 'error' && item.error && (
            <p className="upload-list__error">{item.error}</p>
          )}

          {item.status === 'ready' && item.documentId && (
            <p className="upload-list__success">ID: {item.documentId}</p>
          )}
        </li>
      ))}
    </ul>
  )
}
