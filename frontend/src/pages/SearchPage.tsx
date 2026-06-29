import { useCallback, useState, type FormEvent } from 'react'
import { isSearchMockEnabled, searchDocuments } from '../api/client'
import { Pagination } from '../components/Pagination'
import { SearchResultCard } from '../components/SearchResultCard'
import type { SearchResponse } from '../types/api'

const PAGE_SIZE = 10

export function SearchPage() {
  const [query, setQuery] = useState('')
  const [submittedQuery, setSubmittedQuery] = useState('')
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [response, setResponse] = useState<SearchResponse | null>(null)

  const runSearch = useCallback(async (nextQuery: string, nextPage: number) => {
    const trimmed = nextQuery.trim()
    if (!trimmed) {
      setResponse(null)
      setError(null)
      setSubmittedQuery('')
      return
    }

    setLoading(true)
    setError(null)
    setSubmittedQuery(trimmed)
    setPage(nextPage)

    try {
      const data = await searchDocuments(trimmed, nextPage, PAGE_SIZE)
      setResponse(data)
    } catch (searchError) {
      setResponse(null)
      setError(searchError instanceof Error ? searchError.message : 'Не удалось выполнить поиск')
    } finally {
      setLoading(false)
    }
  }, [])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    void runSearch(query, 1)
  }

  const handlePageChange = (nextPage: number) => {
    if (!submittedQuery) {
      return
    }

    void runSearch(submittedQuery, nextPage)
  }

  return (
    <>
      <section className="panel">
        <div className="panel__header">
          <div>
            <h2>Поиск по документам</h2>
            <p className="panel__hint">
              {isSearchMockEnabled()
                ? 'Сейчас используются mock-данные. Когда backend добавит GET /api/v1/search, установите VITE_SEARCH_MOCK=false.'
                : 'Запросы отправляются на GET /api/v1/search.'}
            </p>
          </div>
          {isSearchMockEnabled() && <span className="mock-badge">Mock</span>}
        </div>

        <form className="search-form" onSubmit={handleSubmit}>
          <input
            className="search-form__input"
            type="search"
            value={query}
            placeholder="Введите запрос…"
            onChange={(event) => setQuery(event.target.value)}
          />
          <button className="button button--primary search-form__button" type="submit" disabled={loading}>
            {loading ? 'Поиск…' : 'Найти'}
          </button>
        </form>
      </section>

      <section className="panel">
        {error && <p className="panel__error">{error}</p>}

        {!error && submittedQuery && response && response.total === 0 && (
          <p className="empty-state">
            Ничего не найдено по запросу «{submittedQuery}». Попробуйте другие ключевые слова.
          </p>
        )}

        {!error && response && response.results.length > 0 && (
          <>
            <p className="results-summary">
              Найдено {response.total} фрагментов по запросу «{response.query}»
            </p>
            <div className="results-list">
              {response.results.map((item) => (
                <SearchResultCard key={item.chunk_id} item={item} query={response.query} />
              ))}
            </div>
            <Pagination
              page={page}
              pageSize={PAGE_SIZE}
              total={response.total}
              onPageChange={handlePageChange}
            />
          </>
        )}

        {!submittedQuery && !loading && (
          <p className="empty-state">Введите запрос и нажмите «Найти» или Enter.</p>
        )}
      </section>
    </>
  )
}
