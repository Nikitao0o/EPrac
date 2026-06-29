import { useRef, useState } from 'react'

interface FileDropzoneProps {
  onFilesSelected: (files: File[]) => void
  disabled?: boolean
}

export function FileDropzone({ onFilesSelected, disabled = false }: FileDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragActive, setDragActive] = useState(false)

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList || disabled) {
      return
    }

    onFilesSelected(Array.from(fileList))
  }

  return (
    <div
      className={`dropzone${dragActive ? ' dropzone--active' : ''}${disabled ? ' dropzone--disabled' : ''}`}
      onDragEnter={(event) => {
        event.preventDefault()
        if (!disabled) {
          setDragActive(true)
        }
      }}
      onDragOver={(event) => {
        event.preventDefault()
      }}
      onDragLeave={(event) => {
        event.preventDefault()
        setDragActive(false)
      }}
      onDrop={(event) => {
        event.preventDefault()
        setDragActive(false)
        handleFiles(event.dataTransfer.files)
      }}
    >
      <input
        ref={inputRef}
        className="dropzone__input"
        type="file"
        accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        multiple
        disabled={disabled}
        onChange={(event) => handleFiles(event.target.files)}
      />
      <p className="dropzone__title">Перетащите PDF или DOCX сюда</p>
      <p className="dropzone__hint">Можно выбрать несколько файлов, максимум 20 МБ каждый</p>
      <button
        type="button"
        className="button button--secondary"
        disabled={disabled}
        onClick={() => inputRef.current?.click()}
      >
        Выбрать файлы
      </button>
    </div>
  )
}
