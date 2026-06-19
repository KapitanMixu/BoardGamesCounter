import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, isAdmin, type GameSession, type Game, type Player } from '../api/client'

interface ScoreEntry {
  player_id: number
  points: string
  winner: boolean
}

type SortKey = 'date' | 'game'

function sortSessions(sessions: GameSession[], key: SortKey, gamesMap: Record<number, Game>): GameSession[] {
  const sorted = sessions.slice()
  if (key === 'game') {
    sorted.sort((a, b) => {
      const an = gamesMap[a.game_id]?.name ?? ''
      const bn = gamesMap[b.game_id]?.name ?? ''
      return an.localeCompare(bn, 'pl') || b.played_at.localeCompare(a.played_at)
    })
  } else {
    // najnowsze pierwsze
    sorted.sort((a, b) => b.played_at.localeCompare(a.played_at))
  }
  return sorted
}

export default function SessionList() {
  const [sessions, setSessions] = useState<GameSession[]>([])
  const [gamesMap, setGamesMap] = useState<Record<number, Game>>({})
  const [gamesList, setGamesList] = useState<Game[]>([])
  const [allPlayers, setAllPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [formOpen, setFormOpen] = useState(false)
  const [selectedGameId, setSelectedGameId] = useState<number | ''>('')
  const [sessionName, setSessionName] = useState('')
  const [notes, setNotes] = useState('')
  const [scores, setScores] = useState<ScoreEntry[]>([])
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)
  const [newPlayerName, setNewPlayerName] = useState('')
  const [addingPlayer, setAddingPlayer] = useState(false)
  const [sortKey, setSortKey] = useState<SortKey>('date')
  const [search, setSearch] = useState('')

  useEffect(() => {
    Promise.all([api.sessions.list(), api.games.list(), api.players.list()])
      .then(([s, g, p]) => {
        setSessions(s)
        setGamesMap(Object.fromEntries(g.map(game => [game.id, game])))
        setGamesList(g)
        setAllPlayers(p)
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  function openForm() {
    setFormOpen(true)
    setSelectedGameId('')
    setSessionName('')
    setNotes('')
    setScores([])
    setFormError(null)
  }

  function togglePlayer(player: Player) {
    setScores(prev => {
      const exists = prev.find(s => s.player_id === player.id)
      if (exists) return prev.filter(s => s.player_id !== player.id)
      return [...prev, { player_id: player.id, points: '', winner: false }]
    })
  }

  function updateScore(player_id: number, field: 'points' | 'winner', value: string | boolean) {
    setScores(prev => prev.map(s => s.player_id === player_id ? { ...s, [field]: value } : s))
  }

  async function handleAddNewPlayer() {
    const name = newPlayerName.trim()
    if (!name) return
    setAddingPlayer(true)
    try {
      const player = await api.players.create({ name })
      setAllPlayers(prev => [...prev, player])
      setScores(prev => [...prev, { player_id: player.id, points: '', winner: false }])
      setNewPlayerName('')
    } finally {
      setAddingPlayer(false)
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!selectedGameId) { setFormError('Wybierz grę'); return }
    setSubmitting(true)
    setFormError(null)
    try {
      const session = await api.sessions.create({
        game_id: Number(selectedGameId),
        name: sessionName.trim() || null,
        notes: notes.trim() || null,
        scores: scores.map(s => ({
          player_id: s.player_id,
          points: s.points !== '' ? Number(s.points) : null,
          winner: s.winner,
        })),
      })
      setSessions(prev => [session, ...prev])
      setFormOpen(false)
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>

  return (
    <section className="session-list">
      <div className="detail-card-header" style={{ marginBottom: '1rem' }}>
        <h2>Sesje ({sessions.length})</h2>
        {isAdmin() && !formOpen && <button onClick={openForm}>+ Dodaj sesję</button>}
      </div>

      <input
        type="search"
        className="search-input"
        placeholder="Szukaj sesji, gry lub gracza..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      <div className="filter-tabs">
        <label className="sort-control">
          Sortuj:
          <select value={sortKey} onChange={e => setSortKey(e.target.value as SortKey)}>
            <option value="date">Data (najnowsze)</option>
            <option value="game">Gra (A-Z)</option>
          </select>
        </label>
      </div>

      {formOpen && (
        <div className="detail-card" style={{ marginBottom: '1.5rem' }}>
          <form className="session-form" onSubmit={handleSubmit}>
            <h4>Nowa sesja</h4>

            <select
              value={selectedGameId}
              onChange={e => {
                const id = Number(e.target.value)
                setSelectedGameId(id)
                const gameSessions = sessions.filter(s => s.game_id === id)
                const gameName = gamesMap[id]?.name ?? `Gra #${id}`
                setSessionName(`${gameName} Sesja #${gameSessions.length + 1}`)
              }}
              className="session-notes-input"
              style={{ marginBottom: '0.75rem' }}
              required
            >
              <option value="">-- Wybierz grę --</option>
              {gamesList.map(g => (
                <option key={g.id} value={g.id}>{g.name}</option>
              ))}
            </select>

            <input
              type="text"
              placeholder="Nazwa sesji"
              value={sessionName}
              onChange={e => setSessionName(e.target.value)}
              className="session-notes-input"
              style={{ marginBottom: '0.75rem' }}
            />

            <div className="session-players">
              <p className="form-label">Uczestnicy:</p>
              {allPlayers.map(player => {
                const entry = scores.find(s => s.player_id === player.id)
                return (
                  <div key={player.id} className="session-player-row">
                    <label className="player-checkbox">
                      <input type="checkbox" checked={!!entry} onChange={() => togglePlayer(player)} />
                      <span>{player.name}</span>
                    </label>
                    {entry && (
                      <div className="player-score-inputs">
                        <input
                          type="number"
                          placeholder="Punkty"
                          value={entry.points}
                          onChange={e => updateScore(player.id, 'points', e.target.value)}
                        />
                        <label className="winner-check">
                          <input
                            type="checkbox"
                            checked={entry.winner}
                            onChange={e => updateScore(player.id, 'winner', e.target.checked)}
                          />
                          Zwycięzca
                        </label>
                      </div>
                    )}
                  </div>
                )
              })}
              <div className="add-player-inline">
                <input
                  type="text"
                  placeholder="Nowy gracz..."
                  value={newPlayerName}
                  onChange={e => setNewPlayerName(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), handleAddNewPlayer())}
                />
                <button
                  type="button"
                  className="btn-add-expansion"
                  disabled={!newPlayerName.trim() || addingPlayer}
                  onClick={handleAddNewPlayer}
                >{addingPlayer ? '...' : '+ Dodaj'}</button>
              </div>
            </div>

            <input
              type="text"
              placeholder="Notatki (opcjonalnie)"
              value={notes}
              onChange={e => setNotes(e.target.value)}
              className="session-notes-input"
            />

            {formError && <p className="form-error">{formError}</p>}

            <div className="form-row" style={{ marginTop: '0.75rem' }}>
              <button type="submit" disabled={submitting || !selectedGameId}>
                {submitting ? 'Zapisywanie...' : 'Zapisz sesję'}
              </button>
              <button type="button" className="btn-cancel" onClick={() => setFormOpen(false)}>Anuluj</button>
            </div>
          </form>
        </div>
      )}

      <ul>
        {sortSessions(
          sessions.filter(s => {
            const q = search.trim().toLowerCase()
            if (!q) return true
            const name = (s.name ?? '').toLowerCase()
            const gameName = (gamesMap[s.game_id]?.name ?? '').toLowerCase()
            const playerMatch = s.scores.some(sc => sc.player.name.toLowerCase().includes(q))
            return name.includes(q) || gameName.includes(q) || playerMatch
          }),
          sortKey,
          gamesMap,
        ).map(session => (
          <li key={session.id} className="session-card">
            <div className="session-header">
              <div className="session-header-main">
                {gamesMap[session.game_id]?.thumbnail_url
                  ? <img src={gamesMap[session.game_id].thumbnail_url!} alt="" className="game-thumb session-thumb" />
                  : <span className="game-thumb session-thumb game-thumb-placeholder">{(gamesMap[session.game_id]?.name ?? '?').charAt(0).toUpperCase()}</span>}
                <div>
                  <Link to={`/sessions/${session.id}`} className="session-name">{session.name ?? `Sesja #${session.id}`}</Link>
                  {gamesMap[session.game_id]
                    ? <Link to={`/games/${session.game_id}`} className="game-chip">🎲 {gamesMap[session.game_id].name}</Link>
                    : <span className="game-chip">🎲 Gra #{session.game_id}</span>}
                </div>
              </div>
              <span className="session-date">{new Date(session.played_at).toLocaleDateString('pl-PL')}</span>
            </div>
            {session.notes && <p className="session-notes">{session.notes}</p>}
            {session.scores.length > 0 && (
              <ul className="score-list">
                {session.scores.map(score => (
                  <li key={score.id} className={`score-item${score.winner ? ' winner' : ''}`}>
                    <Link to={`/players/${score.player.id}`} className="bar-label">{score.player.name}</Link>
                    {score.points != null && <span>{score.points} pkt</span>}
                    {score.winner && <span className="winner-crown" title="Zwycięzca">👑</span>}
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </section>
  )
}
