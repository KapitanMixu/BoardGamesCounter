import { useEffect, useState } from 'react'
import { api, linkPlayer, type Player } from '../api/client'

interface Props {
  onLinked: () => void
}

export default function PlayerPicker({ onLinked }: Props) {
  const [players, setPlayers] = useState<Player[]>([])
  const [choice, setChoice] = useState<'existing' | 'new'>('existing')
  const [selectedId, setSelectedId] = useState<number | ''>('')
  const [newName, setNewName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.players.list().then(setPlayers).catch(() => {})
  }, [])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      if (choice === 'existing') {
        if (selectedId === '') { setError('Wybierz gracza'); setLoading(false); return }
        await linkPlayer({ player_id: selectedId as number })
      } else {
        const name = newName.trim()
        if (!name) { setError('Podaj nazwę'); setLoading(false); return }
        await linkPlayer({ player_name: name })
      }
      onLinked()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrapper">
      <h1>Board Games Counter</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <h2 style={{ marginBottom: '1rem', fontSize: '1.1rem', color: 'var(--color-text-muted)' }}>
          Kim jesteś?
        </h2>
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab${choice === 'existing' ? ' active' : ''}`}
            onClick={() => setChoice('existing')}
          >Istniejący gracz</button>
          <button
            type="button"
            className={`auth-tab${choice === 'new' ? ' active' : ''}`}
            onClick={() => setChoice('new')}
          >Nowy gracz</button>
        </div>

        {choice === 'existing' ? (
          <label>
            Gracz
            <select
              value={selectedId}
              onChange={e => setSelectedId(e.target.value === '' ? '' : Number(e.target.value))}
              required
            >
              <option value="">— wybierz —</option>
              {players.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </label>
        ) : (
          <label>
            Twoja nazwa gracza
            <input
              type="text"
              value={newName}
              onChange={e => setNewName(e.target.value)}
              placeholder="np. Mikołaj"
              autoFocus
            />
          </label>
        )}

        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? '...' : 'Dalej'}
        </button>
      </form>
    </div>
  )
}
