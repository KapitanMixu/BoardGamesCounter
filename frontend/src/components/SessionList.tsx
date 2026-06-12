import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type GameSession, type Game, type Player } from '../api/client'

interface ScoreEntry {
  player_id: number
  points: string
  winner: boolean
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
        {!formOpen && <button onClick={openForm}>+ Dodaj sesję</button>}
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
                setSessionName(`Rozgrywka#${gameSessions.length + 1}`)
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
        {sessions.map(session => (
          <li key={session.id} className="session-card">
            <div className="session-header">
              <div>
                <Link to={`/sessions/${session.id}`} className="session-name">{session.name ?? `Sesja #${session.id}`}</Link>
                <span className="session-game-link">
                  {gamesMap[session.game_id]
                    ? <Link to={`/games/${session.game_id}`}>{gamesMap[session.game_id].name}</Link>
                    : `Gra #${session.game_id}`}
                </span>
              </div>
              <span className="session-date">{session.played_at}</span>
            </div>
            {session.notes && <p className="session-notes">{session.notes}</p>}
            {session.scores.length > 0 && (
              <ul className="score-list">
                {session.scores.map(score => (
                  <li key={score.id} className={`score-item${score.winner ? ' winner' : ''}`}>
                    <span>{score.player.name}</span>
                    {score.points != null && <span>{score.points} pkt</span>}
                    {score.winner && <span className="winner-badge">Zwycięzca</span>}
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
