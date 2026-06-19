import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, isAdmin, type Player } from '../api/client'

function plPlural(n: number, one: string, few: string, many: string): string {
  const m10 = n % 10, m100 = n % 100
  if (n === 1) return one
  if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return few
  return many
}

export default function PlayerList() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [name, setName] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)
  const [search, setSearch] = useState('')

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
      {isAdmin() && (
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
      )}
      <h2>Gracze ({players.length})</h2>
      <input
        type="search"
        className="search-input"
        placeholder="Szukaj gracza..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <ul>
        {players
          .filter(p => {
            const q = search.trim().toLowerCase()
            return !q || p.name.toLowerCase().includes(q)
          })
          .map(player => (
          <li key={player.id} className="player-card">
            <Link to={`/players/${player.id}`} className="player-name game-name">{player.name}</Link>
            <div className="player-card-stats">
              <span>🎲 {player.total_plays} {plPlural(player.total_plays, 'gra', 'gry', 'gier')}</span>
              <span>👑 {player.total_wins} {plPlural(player.total_wins, 'wygrana', 'wygrane', 'wygranych')}</span>
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}
