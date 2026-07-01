import type { SearchResponse } from '../types/api'

const MOCK_CHUNKS = [
  {
    chunk_id: 'mock-1',
    file_name: 'lecture-01.pdf',
    page: 3,
    text: 'Elasticsearch поддерживает полнотекстовый поиск с морфологическим анализом русского языка через analyzer russian.',
    score: 0.92,
  },
  {
    chunk_id: 'mock-2',
    file_name: 'lecture-02.pdf',
    page: 7,
    text: 'FastAPI позволяет быстро описывать REST API с автоматической генерацией OpenAPI и Swagger UI.',
    score: 0.88,
  },
  {
    chunk_id: 'mock-3',
    file_name: 'notes.docx',
    page: 1,
    text: 'Документы разбиваются на чанки длиной 1000 символов с overlap 100 для более точного поиска.',
    score: 0.81,
  },
  {
    chunk_id: 'mock-4',
    file_name: 'lecture-03.pdf',
    page: 12,
    text: 'Docker Compose объединяет backend, frontend, PostgreSQL, Redis и Elasticsearch в одном окружении.',
    score: 0.79,
  },
  {
    chunk_id: 'mock-5',
    file_name: 'lecture-04.pdf',
    page: 5,
    text: 'Prometheus собирает метрики времени ответа search endpoint и помогает отслеживать деградацию сервиса.',
    score: 0.74,
  },
  {
    chunk_id: 'mock-6',
    file_name: 'lecture-05.pdf',
    page: 2,
    text: 'React и Vite дают быстрый dev-сервер и сборку SPA, а Nginx проксирует /api на backend.',
    score: 0.71,
  },
  {
    chunk_id: 'mock-7',
    file_name: 'lab-guide.docx',
    page: 4,
    text: 'Загрузка PDF и DOCX проходит валидацию по расширению, content-type и максимальному размеру 20 МБ.',
    score: 0.68,
  },
  {
    chunk_id: 'mock-8',
    file_name: 'lecture-06.pdf',
    page: 9,
    text: 'Multi-match запрос в Elasticsearch ищет совпадения сразу по нескольким полям индекса documents.',
    score: 0.65,
  },
  {
    chunk_id: 'mock-9',
    file_name: 'lecture-07.pdf',
    page: 15,
    text: 'Playwright используется для E2E сценариев: загрузка документа, индексация, поиск и проверка карточек.',
    score: 0.62,
  },
  {
    chunk_id: 'mock-10',
    file_name: 'lecture-08.pdf',
    page: 6,
    text: 'Redis может кешировать популярные search-запросы и снижать нагрузку на Elasticsearch.',
    score: 0.59,
  },
  {
    chunk_id: 'mock-11',
    file_name: 'lecture-09.pdf',
    page: 11,
    text: 'Grafana визуализирует метрики Prometheus и помогает команде следить за SLA поискового сервиса.',
    score: 0.55,
  },
  {
    chunk_id: 'mock-12',
    file_name: 'lecture-10.pdf',
    page: 8,
    text: 'Precision@3 оценивает качество поиска: насколько релевантны первые три результата для тестового запроса.',
    score: 0.51,
  },
]

function scoreChunk(query: string, text: string): number {
  const terms = query.toLowerCase().split(/\s+/).filter(Boolean)
  const haystack = text.toLowerCase()
  let matches = 0

  for (const term of terms) {
    if (haystack.includes(term)) {
      matches += 1
    }
  }

  if (matches === 0) {
    return 0
  }

  return matches / terms.length
}

export function mockSearch(query: string, page: number, pageSize: number): Promise<SearchResponse> {
  const ranked = MOCK_CHUNKS.map((chunk) => ({
    ...chunk,
    score: scoreChunk(query, chunk.text) * chunk.score,
  }))
    .filter((chunk) => chunk.score > 0)
    .sort((a, b) => b.score - a.score)

  const start = (page - 1) * pageSize
  const results = ranked.slice(start, start + pageSize)

  return Promise.resolve({
    query,
    total: ranked.length,
    page,
    page_size: pageSize,
    results,
  })
}
