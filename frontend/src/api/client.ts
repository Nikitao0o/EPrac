import type { HealthResponse, SearchResponse, UploadResponse } from '../types/api'
import { mockSearch } from './mockSearch'

const API_BASE = '/api/v1'
const SEARCH_USE_MOCK = import.meta.env.VITE_SEARCH_MOCK !== 'false'

function parseApiError(body: string, status: number): string {
  try {
    const data = JSON.parse(body) as { detail?: string | Array<{ msg?: string }> }
    if (typeof data.detail === 'string') {
      return data.detail
    }
    if (Array.isArray(data.detail)) {
      return data.detail.map((item) => item.msg ?? 'Ошибка валидации').join('; ')
    }
  } catch {
    // ignore JSON parse errors
  }

  return body || `HTTP ${status}`
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init)

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(parseApiError(detail, response.status))
  }

  return response.json() as Promise<T>
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>('/healthcheck')
}

export function uploadDocumentWithProgress(
  file: File,
  onProgress: (percent: number) => void,
): Promise<UploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', `${API_BASE}/documents/upload`)

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        onProgress(Math.round((event.loaded / event.total) * 100))
      }
    }

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText) as UploadResponse)
        return
      }

      reject(new Error(parseApiError(xhr.responseText, xhr.status)))
    }

    xhr.onerror = () => reject(new Error('Не удалось загрузить файл. Проверьте соединение.'))

    const formData = new FormData()
    formData.append('file', file)
    xhr.send(formData)
  })
}

export async function searchDocuments(
  query: string,
  page = 1,
  pageSize = 10,
): Promise<SearchResponse> {
  const trimmed = query.trim()
  if (!trimmed) {
    return { query: trimmed, total: 0, page, page_size: pageSize, results: [] }
  }

  if (SEARCH_USE_MOCK) {
    return mockSearch(trimmed, page, pageSize)
  }

  const params = new URLSearchParams({
    q: trimmed,
    page: String(page),
    page_size: String(pageSize),
  })

  return request<SearchResponse>(`/search?${params.toString()}`)
}

export function isSearchMockEnabled(): boolean {
  return SEARCH_USE_MOCK
}
