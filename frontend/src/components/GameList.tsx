import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, isAdmin, type Game, type DurationType, type Expansion, type ExpansionUpdate } from '../api/client'
import AddGameForm from './AddGameForm'

function formatDuration(minutes: number, type: DurationType): string {
  return type === 'per_player' ? `${minutes} min/gracza` : `${minutes} min`
}

interface GameCardProps {
  game: Game
}

function GameCard({ game }: GameCardProps) {
  const admin = isAdmin()
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
        {game.thumbnail_url
          ? <img src={game.thumbnail_url} alt="" className="game-thumb" loading="lazy" />
          : <span className="game-thumb game-thumb-placeholder">{game.name.charAt(0).toUpperCase()}</span>}
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
                        {admin && <button className="btn-edit-inline" onClick={() => { setEditingExpId(exp.id); setEditExpName(exp.name) }} title="Edytuj">✎</button>}
                        {admin && <button className="btn-delete" onClick={() => handleDeleteExpansion(exp.id)} title="Usuń">×</button>}
                      </>
                    )}
                  </li>
                ))}
              </ul>
              {admin && (addOpen ? (
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
              ))}
            </>
          )}
        </div>
      )}
    </li>
  )
}

type Filter = 'all' | 'unplayed'
type SortKey = 'last_played' | 'name' | 'max_players'

function sortGames(games: Game[], key: SortKey): Game[] {
  const sorted = games.slice()
  switch (key) {
    case 'name':
      sorted.sort((a, b) => a.name.localeCompare(b.name, 'pl'))
      break
    case 'max_players':
      sorted.sort((a, b) => b.max_players - a.max_players || a.name.localeCompare(b.name, 'pl'))
      break
    case 'last_played':
      // najnowsze pierwsze, nigdy-grane na końcu
      sorted.sort((a, b) => {
        if (!a.last_played_at && !b.last_played_at) return a.name.localeCompare(b.name, 'pl')
        if (!a.last_played_at) return 1
        if (!b.last_played_at) return -1
        return b.last_played_at.localeCompare(a.last_played_at)
      })
      break
  }
  return sorted
}

export default function GameList() {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [modalOpen, setModalOpen] = useState(false)
  const admin = isAdmin()
  const [filter, setFilter] = useState<Filter>('all')
  const [sortKey, setSortKey] = useState<SortKey>('last_played')
  const [search, setSearch] = useState('')

  useEffect(() => {
    api.games.list()
      .then(setGames)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>

  const q = search.trim().toLowerCase()
  const filtered = (filter === 'unplayed' ? games.filter(g => g.times_played === 0) : games)
    .filter(g => !q || g.name.toLowerCase().includes(q))
  const visibleGames = sortGames(filtered, sortKey)

  return (
    <section className="game-list">
      <div className="detail-card-header" style={{ marginBottom: '1rem' }}>
        <h2>Gry ({games.length})</h2>
        {admin && <button onClick={() => setModalOpen(true)}>+ Dodaj grę</button>}
      </div>

      <input
        type="search"
        className="search-input"
        placeholder="Szukaj gry..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div className="filter-tabs">
        <button
          className={`filter-tab${filter === 'all' ? ' active' : ''}`}
          onClick={() => setFilter('all')}
        >
          Wszystkie ({games.length})
        </button>
        <button
          className={`filter-tab${filter === 'unplayed' ? ' active' : ''}`}
          onClick={() => setFilter('unplayed')}
        >
          Niegrane ({games.filter(g => g.times_played === 0).length})
        </button>
        <label className="sort-control">
          Sortuj:
          <select value={sortKey} onChange={e => setSortKey(e.target.value as SortKey)}>
            <option value="last_played">Ostatnia rozgrywka</option>
            <option value="name">Nazwa (A-Z)</option>
            <option value="max_players">Max graczy</option>
          </select>
        </label>
      </div>

      {visibleGames.length === 0 && filter === 'unplayed' && (
        <p className="status">Wszystkie gry były już grane!</p>
      )}

      <ul>
        {visibleGames.map(game => (
          <GameCard key={game.id} game={game} />
        ))}
      </ul>

      {modalOpen && (
        <div className="modal-overlay" onClick={e => { if (e.target === e.currentTarget) setModalOpen(false) }}>
          <div className="modal-box">
            <button className="modal-close" onClick={() => setModalOpen(false)}>✕</button>
            <AddGameForm onAdded={game => { setGames(prev => [...prev, game]); setModalOpen(false) }} />
          </div>
        </div>
      )}
    </section>
  )
}
