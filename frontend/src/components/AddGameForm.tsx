import { useState } from 'react'
import { api, type Game, type DurationType } from '../api/client'

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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setSubmitting(false)
    }
  }

  function openBggSearch() {
    if (name.trim()) {
      window.open(`https://boardgamegeek.com/search/boardgame?q=${encodeURIComponent(name.trim())}`, '_blank', 'noopener')
    }
  }

  return (
    <form className="add-game-form" onSubmit={handleSubmit}>
      <h3>Dodaj grę</h3>
      <div className="form-row">
        <div className="bgg-search-wrapper">
          <input
            type="text"
            placeholder="Nazwa gry"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
          <button
            type="button"
            className="btn-bgg-search"
            onClick={openBggSearch}
            disabled={!name.trim()}
            title="Szukaj na BGG i skopiuj link"
          >BGG ↗</button>
        </div>
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
      <div className="form-row" style={{ marginTop: '0.5rem' }}>
        <input
          type="url"
          placeholder="Link BGG (wklej po wyszukaniu)"
          value={bggUrl}
          onChange={e => setBggUrl(e.target.value)}
          style={{ flex: 1 }}
        />
      </div>
      {error && <p className="form-error">{error}</p>}
    </form>
  )
}
