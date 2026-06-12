import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type Game, type DurationType, type Expansion, type ExpansionUpdate } from '../api/client'
import AddGameForm from './AddGameForm'

function formatDuration(minutes: number, type: DurationType): string {
  return type === 'per_player' ? `${minutes} min/gracza` : `${minutes} min`
}

interface GameCardProps {
  game: Game
}

function GameCard({ game }: GameCardProps) {
  const [open, setOpen] = useState(false)
  const [expansions, setExpansions] = useState<Expansion[]>([])
  const [loadingExp, setLoadingExp] = useState(false)
  const [addOpen, setAddOpen] = useState(false)
  const [expError, setExpError] = useState<string | null>(null)
  const [newExpName, setNewExpName] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [editingExpId, setEditingExpId] = useState<number | null>(null)
  const [editExpName, setEditExpName] = useState('')

  async function handleToggle() {
    if (!open && expansions.length === 0) {
      setLoadingExp(true)
      try {
        const data = await api.expansions.list(game.id)
        setExpansions(data)
      } catch (err) {
        setExpError(err instanceof Error ? err.message : 'Błąd')
      } finally {
        setLoadingExp(false)
      }
    }
    setOpen(prev => !prev)
  }

  async function handleAddExpansion(e: React.FormEvent) {
    e.preventDefault()
    if (!newExpName.trim()) return
    setSubmitting(true)
    try {
      const exp = await api.expansions.create(game.id, { name: newExpName.trim() })
      setExpansions(prev => [...prev, exp])
      setNewExpName('')
      setAddOpen(false)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDeleteExpansion(expansionId: number) {
    await api.expansions.delete(game.id, expansionId)
    setExpansions(prev => prev.filter(e => e.id !== expansionId))
  }

  async function handleEditExpansion(expansionId: number) {
    const name = editExpName.trim()
    if (!name) { setEditingExpId(null); return }
    const updated = await api.expansions.update(game.id, expansionId, { name } as ExpansionUpdate)
    setExpansions(prev => prev.map(e => e.id === expansionId ? updated : e))
    setEditingExpId(null)
  }

  return (
    <li className={`game-card${open ? ' expanded' : ''}`}>
      <div className="game-card-header">
        <Link to={`/games/${game.id}`} className="game-name">{game.name}</Link>
        <div className="game-meta">
          <span>{game.min_players}–{game.max_players} graczy</span>
          {game.duration_minutes && game.duration_type && (
            <span>{formatDuration(game.duration_minutes, game.duration_type)}</span>
          )}
          <span>{game.times_played} {game.times_played === 1 ? 'sesja' : 'sesje'}</span>
          <span>{game.last_played_at ?? 'nigdy nie grane'}</span>
        </div>
        <button className="expand-toggle" onClick={handleToggle}>{open ? '▲' : '▼'}</button>
      </div>

      {open && (
        <div className="expansions-panel">
          {loadingExp ? (
            <p className="status small">Ładowanie...</p>
          ) : expError ? (
            <p className="status small error">Błąd: {expError}</p>
          ) : (
            <>
              <ul className="expansion-list">
                {expansions.length === 0 && (
                  <li className="expansion-empty">Brak dodatków</li>
                )}
                {expansions.map(exp => (
                  <li key={exp.id} className="expansion-item">
                    {editingExpId === exp.id ? (
                      <>
                        <input
                          type="text"
                          value={editExpName}
                          onChange={e => setEditExpName(e.target.value)}
                          onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); handleEditExpansion(exp.id) } if (e.key === 'Escape') setEditingExpId(null) }}
                          autoFocus
                          className="expansion-edit-input"
                        />
                        <button className="btn-save-inline" onClick={() => handleEditExpansion(exp.id)}>✓</button>
                        <button className="btn-cancel-inline" onClick={() => setEditingExpId(null)}>✕</button>
                      </>
                    ) : (
                      <>
                        <span>{exp.name}</span>
                        <button className="btn-edit-inline" onClick={() => { setEditingExpId(exp.id); setEditExpName(exp.name) }} title="Edytuj">✎</button>
                        <button className="btn-delete" onClick={() => handleDeleteExpansion(exp.id)} title="Usuń">×</button>
                      </>
                    )}
                  </li>
                ))}
              </ul>
              {addOpen ? (
                <form className="expansion-add-form" onSubmit={handleAddExpansion}>
                  <input
                    type="text"
                    placeholder="Nazwa dodatku"
                    value={newExpName}
                    onChange={e => setNewExpName(e.target.value)}
                    autoFocus
                  />
                  <button type="submit" disabled={submitting}>Dodaj</button>
                  <button type="button" className="btn-cancel" onClick={() => { setAddOpen(false); setNewExpName('') }}>Anuluj</button>
                </form>
              ) : (
                <button className="btn-add-expansion" onClick={() => setAddOpen(true)}>+ Dodaj dodatek</button>
              )}
            </>
          )}
        </div>
      )}
    </li>
  )
}

export default function GameList() {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.games.list()
      .then(setGames)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>

  return (
    <section className="game-list">
      <AddGameForm onAdded={game => setGames(prev => [...prev, game])} />
      <h2>Gry ({games.length})</h2>
      <ul>
        {games.map(game => (
          <GameCard key={game.id} game={game} />
        ))}
      </ul>
    </section>
  )
}
