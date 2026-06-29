interface HighlightedTextProps {
  text: string
  query: string
}

export function HighlightedText({ text, query }: HighlightedTextProps) {
  const terms = query
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .sort((a, b) => b.length - a.length)

  if (terms.length === 0) {
    return <>{text}</>
  }

  const pattern = new RegExp(`(${terms.map(escapeRegExp).join('|')})`, 'gi')
  const parts = text.split(pattern)

  const lowerTerms = terms.map((term) => term.toLowerCase())

  return (
    <>
      {parts.map((part, index) =>
        lowerTerms.includes(part.toLowerCase()) ? (
          <mark key={`${part}-${index}`} className="highlight">
            {part}
          </mark>
        ) : (
          <span key={`${part}-${index}`}>{part}</span>
        ),
      )}
    </>
  )
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}
