const MAX_FILE_SIZE = 20 * 1024 * 1024
const ALLOWED_EXTENSIONS = ['.pdf', '.docx']

export function validateUploadFile(file: File): string | null {
  const extension = file.name.includes('.')
    ? `.${file.name.split('.').pop()?.toLowerCase()}`
    : ''

  if (!ALLOWED_EXTENSIONS.includes(extension)) {
    return 'Разрешены только PDF и DOCX.'
  }

  if (file.size > MAX_FILE_SIZE) {
    return 'Размер файла превышает 20 МБ.'
  }

  return null
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} B`
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}
