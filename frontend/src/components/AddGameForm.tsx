import { useState, useEffect, useRef } from 'react'
import { api, type Game, type DurationType, type BggResult } from '../api/client'

interface Props {
  onAdded: (game: Game) => void
}

export default function AddGameForm({ onAdded }: Props) {
  const [name, setName] = useState('')
  const [minPlayers, setMinPlayers] = useState(2)
  const [maxPlayers, setMaxPlayers] = useState(4)
  const [durationMinutes, setDurationMinutes] = useState('')
  const [durationType, setDurationType] = useState<DurationType>('total')
  const [bggUrl, setBggUrl] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  // separateSearch=false: name field IS the BGG search (typeahead fills name + link)
  // separateSearch=true: Polish name field + separate English BGG search field
  const [separateSearch, setSeparateSearch] = useState(false)
  const [bggQuery, setBggQuery] = useState('')
  const [bggResults, setBggResults] = useState<BggResult[]>([])
  const [bggLoading, setBggLoading] = useState(false)
  const [showDropdown, setShowDropdown] = useState(false)
  const wrapperRef = useRef<HTMLDivElement>(null)

  const query = separateSearch ? bggQuery : name

  useEffect(() => {
    if (query.trim().length < 2) {
      setBggResults([])
      setShowDropdown(false)
      return
    }
    const timer = setTimeout(async () => {
      setBggLoading(true)
      try {
        const results = await api.bgg.search(query.trim())
        setBggResults(results)
        setShowDropdown(results.length > 0)
      } catch {
        setBggResults([])
        setShowDropdown(false)
      } finally {
        setBggLoading(false)
      }
    }, 400)
    return () => clearTimeout(timer)
  }, [query])

  useEffect(() => {
    function onClickOutside(e: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setShowDropdown(false)
      }
    }
    document.addEventListener('mousedown', onClickOutside)
    return () => document.removeEventListener('mousedown', onClickOutside)
  }, [])

  function selectBggResult(result: BggResult) {
    setBggUrl(result.url)
    if (separateSearch) {
      setBggQuery(result.name)          // English title in search field
      if (!name.trim()) setName(result.name)
    } else {
      setName(result.name)              // name field doubles as search
    }
    setShowDropdown(false)
    setBggResults([])
  }

  function toggleSeparate(checked: boolean) {
    setSeparateSearch(checked)
    setShowDropdown(false)
    setBggResults([])
    if (checked) setBggQuery('')        // start fresh English search
  }

  const dropdown = showDropdown && (
    <ul className="bgg-dropdown">
      {bggResults.map(r => (
        <li key={r.id} className="bgg-dropdown-item" onMouseDown={() => selectBggResult(r)}>
          <span className="bgg-item-name">{r.name}</span>
          {r.year && <span className="bgg-item-year">({r.year})</span>}
        </li>
      ))}
    </ul>
  )

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setSubmitting(true)
    setError(null)
    try {
      const duration = durationMinutes ? Number(durationMinutes) : null
      const game = await api.games.create({
        name: name.trim(),
        min_players: minPlayers,
        max_players: maxPlayers,
        duration_minutes: duration,
        duration_type: duration ? durationType : null,
        bgg_url: bggUrl.trim() || null,
      })
      onAdded(game)
      setName('')
      setMinPlayers(2)
      setMaxPlayers(4)
      setDurationMinutes('')
      setDurationType('total')
      setBggUrl('')
      setBggQuery('')
      setSeparateSearch(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="add-game-form" onSubmit={handleSubmit}>
      <h3>Dodaj grę</h3>
      <div className="form-row">
        {separateSearch ? (
          <input
            type="text"
            placeholder="Nazwa gry (po polsku)"
            value={name}
            onChange={e => setName(e.target.value)}
            required
            style={{ flex: 1, minWidth: 160 }}
          />
        ) : (
          <div className="bgg-search-wrapper" ref={wrapperRef} style={{ flex: 1 }}>
            <input
              type="text"
              placeholder="Nazwa gry (szuka na BGG)"
              value={name}
              onChange={e => { setName(e.target.value); setBggUrl('') }}
              required
            />
            {bggLoading && <span className="bgg-loading">…</span>}
            {dropdown}
          </div>
        )}
        <label>
          Min graczy
          <input type="number" min={1} value={minPlayers} onChange={e => setMinPlayers(Number(e.target.value))} />
        </label>
        <label>
          Max graczy
          <input type="number" min={minPlayers} value={maxPlayers} onChange={e => setMaxPlayers(Number(e.target.value))} />
        </label>
        <label>
          Czas (min)
          <input type="number" min={1} placeholder="opcjonalnie" value={durationMinutes} onChange={e => setDurationMinutes(e.target.value)} />
        </label>
        <div className="duration-type-toggle" aria-disabled={!durationMinutes}>
          <button
            type="button"
            className={`duration-type-btn${durationType === 'total' ? ' active' : ''}`}
            disabled={!durationMinutes}
            onClick={() => setDurationType('total')}
          >łącznie</button>
          <button
            type="button"
            className={`duration-type-btn${durationType === 'per_player' ? ' active' : ''}`}
            disabled={!durationMinutes}
            onClick={() => setDurationType('per_player')}
          >na gracza</button>
        </div>
        <button type="submit" disabled={submitting}>
          {submitting ? 'Dodawanie...' : 'Dodaj'}
        </button>
      </div>

      <label className="english-search-toggle">
        <input
          type="checkbox"
          checked={separateSearch}
          onChange={e => toggleSeparate(e.target.checked)}
        />
        Polska nazwa inna niż na BGG (szukaj osobno po angielsku)
      </label>

      {separateSearch && (
        <div className="form-row" style={{ marginTop: '0.5rem' }}>
          <div className="bgg-search-wrapper" ref={wrapperRef} style={{ flex: 1 }}>
            <input
              type="text"
              placeholder="Angielska nazwa do wyszukania na BGG..."
              value={bggQuery}
              onChange={e => { setBggQuery(e.target.value); setBggUrl('') }}
            />
            {bggLoading && <span className="bgg-loading">…</span>}
            {dropdown}
          </div>
        </div>
      )}

      {bggUrl && (
        <div className="form-row" style={{ marginTop: '0.5rem' }}>
          <span className="bgg-url-preview">
            BGG: <a href={bggUrl} target="_blank" rel="noopener noreferrer" className="bgg-link">{bggUrl}</a>
          </span>
        </div>
      )}
      {error && <p className="form-error">{error}</p>}
    </form>
  )
}
