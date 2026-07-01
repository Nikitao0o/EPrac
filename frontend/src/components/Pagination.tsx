interface PaginationProps {
  page: number
  pageSize: number
  total: number
  onPageChange: (page: number) => void
}

export function Pagination({ page, pageSize, total, onPageChange }: PaginationProps) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  if (totalPages <= 1) {
    return null
  }

  return (
    <nav className="pagination" aria-label="Навигация по страницам результатов">
      <button
        type="button"
        className="pagination__button"
        disabled={page <= 1}
        onClick={() => onPageChange(page - 1)}
      >
        Назад
      </button>
      <span className="pagination__info">
        Страница {page} из {totalPages}
      </span>
      <button
        type="button"
        className="pagination__button"
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
      >
        Вперёд
      </button>
    </nav>
  )
}
