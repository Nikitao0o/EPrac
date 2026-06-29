export interface UploadResponse {
  message: string
  document_id: string
  filename: string
  size_bytes: number
}

export interface HealthResponse {
  status: string
  message?: string
}

export interface SearchResultItem {
  chunk_id: string
  file_name: string
  page: number
  text: string
  score: number
}

export interface SearchResponse {
  query: string
  total: number
  page: number
  page_size: number
  results: SearchResultItem[]
}

export type UploadStatus = 'pending' | 'uploading' | 'indexing' | 'ready' | 'error'

export interface UploadItem {
  localId: string
  file: File
  status: UploadStatus
  progress: number
  documentId?: string
  error?: string
  uploadedAt?: Date
}
