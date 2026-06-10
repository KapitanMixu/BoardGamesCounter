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
      })
      onAdded(game)
      setName('')
      setMinPlayers(2)
      setMaxPlayers(4)
      setDurationMinutes('')
      setDurationType('total')
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
        <input
          type="text"
          placeholder="Nazwa gry"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <label>
          Min graczy
          <input
            type="number"
            min={1}
            value={minPlayers}
            onChange={e => setMinPlayers(Number(e.target.value))}
          />
        </label>
        <label>
          Max graczy
          <input
            type="number"
            min={minPlayers}
            value={maxPlayers}
            onChange={e => setMaxPlayers(Number(e.target.value))}
          />
        </label>
        <label>
          Czas (min)
          <input
            type="number"
            min={1}
            placeholder="opcjonalnie"
            value={durationMinutes}
            onChange={e => setDurationMinutes(e.target.value)}
          />
        </label>
        <label>
          Typ czasu
          <select
            value={durationType}
            onChange={e => setDurationType(e.target.value as DurationType)}
            disabled={!durationMinutes}
          >
            <option value="total">łącznie</option>
            <option value="per_player">na gracza</option>
          </select>
        </label>
        <button type="submit" disabled={submitting}>
          {submitting ? 'Dodawanie...' : 'Dodaj'}
        </button>
      </div>
      {error && <p className="form-error">{error}</p>}
    </form>
  )
}
