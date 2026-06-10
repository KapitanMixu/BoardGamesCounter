import { useEffect, useState } from 'react'
import { api, type Player } from '../api/client'

export default function PlayerList() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [name, setName] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  useEffect(() => {
    api.players.list()
      .then(setPlayers)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setSubmitting(true)
    setFormError(null)
    try {
      const player = await api.players.create({ name: name.trim() })
      setPlayers(prev => [...prev, player])
      setName('')
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>

  return (
    <section className="player-list">
      <form className="add-inline-form" onSubmit={handleSubmit}>
        <h3>Dodaj gracza</h3>
        <div className="form-row">
          <input
            type="text"
            placeholder="Nazwa gracza"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
          <button type="submit" disabled={submitting}>
            {submitting ? 'Dodawanie...' : 'Dodaj'}
          </button>
        </div>
        {formError && <p className="form-error">{formError}</p>}
      </form>
      <h2>Gracze ({players.length})</h2>
      <ul>
        {players.map(player => (
          <li key={player.id} className="player-card">
            <span className="player-name">{player.name}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}
