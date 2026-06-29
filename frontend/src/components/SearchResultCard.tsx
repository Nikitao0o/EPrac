import type { SearchResultItem } from '../types/api'
import { HighlightedText } from './HighlightedText'

interface SearchResultCardProps {
  item: SearchResultItem
  query: string
}

export function SearchResultCard({ item, query }: SearchResultCardProps) {
  return (
    <article className="result-card">
      <header className="result-card__header">
        <div>
          <h3 className="result-card__title">{item.file_name}</h3>
          <p className="result-card__meta">Страница {item.page}</p>
        </div>
        <span className="result-card__score">{(item.score * 100).toFixed(0)}%</span>
      </header>
      <p className="result-card__text">
        <HighlightedText text={item.text} query={query} />
      </p>
    </article>
  )
}
