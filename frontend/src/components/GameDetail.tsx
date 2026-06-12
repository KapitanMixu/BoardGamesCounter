import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api, type Game, type GameSession, type Expansion, type Player, type DurationType } from '../api/client'

interface PlayerStat {
  name: string
  plays: number
  wins: number
}

function computeStats(sessions: GameSession[]): PlayerStat[] {
  const map: Record<number, PlayerStat> = {}
  for (const s of sessions) {
    for (const score of s.scores) {
      const pid = score.player.id
      if (!map[pid]) map[pid] = { name: score.player.name, plays: 0, wins: 0 }
      map[pid].plays++
      if (score.winner) map[pid].wins++
    }
  }
  return Object.values(map).sort((a, b) => b.wins - a.wins || b.plays - a.plays)
}

interface ScoreEntry {
  player_id: number
  points: string
  winner: boolean
}

export default function GameDetail() {
  const { id } = useParams<{ id: string }>()
  const gameId = Number(id)

  const [game, setGame] = useState<Game | null>(null)
  const [sessions, setSessions] = useState<GameSession[]>([])
  const [expansions, setExpansions] = useState<Expansion[]>([])
  const [allPlayers, setAllPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // game edit
  const [gameEditOpen, setGameEditOpen] = useState(false)
  const [editName, setEditName] = useState('')
  const [editMinPlayers, setEditMinPlayers] = useState('')
  const [editMaxPlayers, setEditMaxPlayers] = useState('')
  const [editDurationMinutes, setEditDurationMinutes] = useState('')
  const [editDurationType, setEditDurationType] = useState<DurationType | ''>('')
  const [gameEditSaving, setGameEditSaving] = useState(false)

  // expansions
  const [newExpName, setNewExpName] = useState('')
  const [addExpOpen, setAddExpOpen] = useState(false)
  const [expSubmitting, setExpSubmitting] = useState(false)
  const [editingExpId, setEditingExpId] = useState<number | null>(null)
  const [editExpName, setEditExpName] = useState('')

  // new session form
  const [sessionFormOpen, setSessionFormOpen] = useState(false)
  const [sessionName, setSessionName] = useState('')
  const [notes, setNotes] = useState('')
  const [scores, setScores] = useState<ScoreEntry[]>([])
  const [sessionSubmitting, setSessionSubmitting] = useState(false)
  const [sessionError, setSessionError] = useState<string | null>(null)
  const [newPlayerName, setNewPlayerName] = useState('')
  const [addingPlayer, setAddingPlayer] = useState(false)

  // session edit
  const [editingSessionId, setEditingSessionId] = useState<number | null>(null)
  const [editSessionName, setEditSessionName] = useState('')
  const [editSessionNotes, setEditSessionNotes] = useState('')
  const [sessionEditSaving, setSessionEditSaving] = useState(false)

  useEffect(() => {
    Promise.all([
      api.games.get(gameId),
      api.games.sessions(gameId),
      api.expansions.list(gameId),
      api.players.list(),
    ])
      .then(([g, s, e, p]) => { setGame(g); setSessions(s); setExpansions(e); setAllPlayers(p) })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [gameId])

  function openGameEdit() {
    if (!game) return
    setEditName(game.name)
    setEditMinPlayers(String(game.min_players))
    setEditMaxPlayers(String(game.max_players))
    setEditDurationMinutes(game.duration_minutes != null ? String(game.duration_minutes) : '')
    setEditDurationType(game.duration_type ?? '')
    setGameEditOpen(true)
  }

  async function handleGameEdit(e: React.FormEvent) {
    e.preventDefault()
    setGameEditSaving(true)
    try {
      const updated = await api.games.update(gameId, {
        name: editName.trim() || undefined,
        min_players: editMinPlayers ? Number(editMinPlayers) : undefined,
        max_players: editMaxPlayers ? Number(editMaxPlayers) : undefined,
        duration_minutes: editDurationMinutes ? Number(editDurationMinutes) : null,
        duration_type: editDurationType || null,
      })
      setGame(updated)
      setGameEditOpen(false)
    } finally {
      setGameEditSaving(false)
    }
  }

  async function handleAddExpansion(e: React.FormEvent) {
    e.preventDefault()
    if (!newExpName.trim()) return
    setExpSubmitting(true)
    try {
      const exp = await api.expansions.create(gameId, { name: newExpName.trim() })
      setExpansions(prev => [...prev, exp])
      setNewExpName('')
      setAddExpOpen(false)
    } finally {
      setExpSubmitting(false)
    }
  }

  async function handleDeleteExpansion(expId: number) {
    await api.expansions.delete(gameId, expId)
    setExpansions(prev => prev.filter(e => e.id !== expId))
  }

  function openExpEdit(exp: Expansion) {
    setEditingExpId(exp.id)
    setEditExpName(exp.name)
  }

  async function handleExpEdit(expId: number) {
    const name = editExpName.trim()
    if (!name) { setEditingExpId(null); return }
    const updated = await api.expansions.update(gameId, expId, { name })
    setExpansions(prev => prev.map(e => e.id === expId ? updated : e))
    setEditingExpId(null)
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

  async function handleAddSession(e: React.FormEvent) {
    e.preventDefault()
    setSessionSubmitting(true)
    setSessionError(null)
    try {
      const session = await api.sessions.create({
        game_id: gameId,
        name: sessionName.trim() || null,
        notes: notes.trim() || null,
        scores: scores.map(s => ({
          player_id: s.player_id,
          points: s.points !== '' ? Number(s.points) : null,
          winner: s.winner,
        })),
      })
      setSessions(prev => [session, ...prev])
      setSessionFormOpen(false)
      setSessionName('')
      setNotes('')
      setScores([])
    } catch (err) {
      setSessionError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setSessionSubmitting(false)
    }
  }

  function openSessionEdit(s: GameSession) {
    setEditingSessionId(s.id)
    setEditSessionName(s.name ?? '')
    setEditSessionNotes(s.notes ?? '')
  }

  async function handleSessionEdit(e: React.FormEvent) {
    e.preventDefault()
    if (!editingSessionId) return
    setSessionEditSaving(true)
    try {
      const updated = await api.sessions.update(editingSessionId, {
        name: editSessionName.trim() || null,
        notes: editSessionNotes.trim() || null,
      })
      setSessions(prev => prev.map(s => s.id === editingSessionId ? updated : s))
      setEditingSessionId(null)
    } finally {
      setSessionEditSaving(false)
    }
  }

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>
  if (!game) return <p className="status error">Nie znaleziono gry</p>

  const stats = computeStats(sessions)

  return (
    <section className="game-detail">
      <Link to="/games" className="back-link">← Wróć do listy</Link>

      <div className="detail-header">
        {gameEditOpen ? (
          <form className="game-edit-form" onSubmit={handleGameEdit}>
            <div className="form-row">
              <input
                type="text"
                value={editName}
                onChange={e => setEditName(e.target.value)}
                placeholder="Nazwa gry"
                required
              />
            </div>
            <div className="form-row">
              <label>Min graczy
                <input type="number" value={editMinPlayers} onChange={e => setEditMinPlayers(e.target.value)} min={1} style={{ width: '4rem', marginLeft: '0.5rem' }} />
              </label>
              <label>Max graczy
                <input type="number" value={editMaxPlayers} onChange={e => setEditMaxPlayers(e.target.value)} min={1} style={{ width: '4rem', marginLeft: '0.5rem' }} />
              </label>
            </div>
            <div className="form-row">
              <label>Czas (min)
                <input type="number" value={editDurationMinutes} onChange={e => setEditDurationMinutes(e.target.value)} min={1} style={{ width: '5rem', marginLeft: '0.5rem' }} />
              </label>
              <select value={editDurationType} onChange={e => setEditDurationType(e.target.value as DurationType | '')}>
                <option value="">brak</option>
                <option value="total">łącznie</option>
                <option value="per_player">na gracza</option>
              </select>
            </div>
            <div className="form-row" style={{ marginTop: '0.5rem' }}>
              <button type="submit" disabled={gameEditSaving}>{gameEditSaving ? 'Zapisywanie...' : 'Zapisz'}</button>
              <button type="button" className="btn-cancel" onClick={() => setGameEditOpen(false)}>Anuluj</button>
            </div>
          </form>
        ) : (
          <>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <h2>{game.name}</h2>
              <button className="btn-edit-inline" onClick={openGameEdit} title="Edytuj grę">✎</button>
            </div>
            <div className="game-meta">
              <span>{game.min_players}–{game.max_players} graczy</span>
              {game.duration_minutes && game.duration_type && (
                <span>{game.duration_minutes} min{game.duration_type === 'per_player' ? '/gracza' : ''}</span>
              )}
              <span>{sessions.length} rozgrywek</span>
              <span>ostatnio: {game.last_played_at ?? 'nigdy'}</span>
            </div>
          </>
        )}
      </div>

      {/* Dodatki */}
      <div className="detail-card">
        <h3>Dodatki ({expansions.length})</h3>
        {expansions.length > 0 && (
          <ul className="expansion-list" style={{ marginBottom: '0.75rem' }}>
            {expansions.map(exp => (
              <li key={exp.id} className="expansion-item">
                {editingExpId === exp.id ? (
                  <>
                    <input
                      type="text"
                      value={editExpName}
                      onChange={e => setEditExpName(e.target.value)}
                      onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); handleExpEdit(exp.id) } if (e.key === 'Escape') setEditingExpId(null) }}
                      autoFocus
                      className="expansion-edit-input"
                    />
                    <button className="btn-save-inline" onClick={() => handleExpEdit(exp.id)}>✓</button>
                    <button className="btn-cancel-inline" onClick={() => setEditingExpId(null)}>✕</button>
                  </>
                ) : (
                  <>
                    <span>{exp.name}</span>
                    <button className="btn-edit-inline" onClick={() => openExpEdit(exp)} title="Edytuj">✎</button>
                    <button className="btn-delete" onClick={() => handleDeleteExpansion(exp.id)}>×</button>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
        {addExpOpen ? (
          <form className="expansion-add-form" onSubmit={handleAddExpansion}>
            <input
              type="text"
              placeholder="Nazwa dodatku"
              value={newExpName}
              onChange={e => setNewExpName(e.target.value)}
              autoFocus
            />
            <button type="submit" disabled={expSubmitting}>Dodaj</button>
            <button type="button" className="btn-cancel" onClick={() => { setAddExpOpen(false); setNewExpName('') }}>Anuluj</button>
          </form>
        ) : (
          <button className="btn-add-expansion" onClick={() => setAddExpOpen(true)}>+ Dodaj dodatek</button>
        )}
      </div>

      {/* Statystyki */}
      {stats.length > 0 && (
        <div className="detail-card">
          <h3>Statystyki graczy</h3>
          <table className="stats-table">
            <thead>
              <tr><th>Gracz</th><th>Rozgrywki</th><th>Wygrane</th><th>Win %</th></tr>
            </thead>
            <tbody>
              {stats.map(s => (
                <tr key={s.name}>
                  <td>{s.name}</td>
                  <td>{s.plays}</td>
                  <td>{s.wins}</td>
                  <td>{Math.round((s.wins / s.plays) * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Historia rozgrywek */}
      <div className="detail-card">
        <div className="detail-card-header">
          <h3>Historia rozgrywek ({sessions.length})</h3>
          {!sessionFormOpen && (
            <button onClick={() => { setSessionFormOpen(true); setSessionName(`Rozgrywka#${sessions.length + 1}`) }}>+ Dodaj rozgrywkę</button>
          )}
        </div>

        {sessionFormOpen && (
          <form className="session-form" onSubmit={handleAddSession}>
            <h4>Nowa rozgrywka</h4>
            <input
              type="text"
              placeholder="Nazwa rozgrywki"
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
                        <input
                          type="checkbox"
                          checked={!!entry}
                          onChange={() => togglePlayer(player)}
                        />
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
                  >
                    {addingPlayer ? '...' : '+ Dodaj'}
                  </button>
                </div>
              </div>

            <input
              type="text"
              placeholder="Notatki (opcjonalnie)"
              value={notes}
              onChange={e => setNotes(e.target.value)}
              className="session-notes-input"
            />

            {sessionError && <p className="form-error">{sessionError}</p>}

            <div className="form-row" style={{ marginTop: '0.75rem' }}>
              <button type="submit" disabled={sessionSubmitting || scores.length === 0}>
                {sessionSubmitting ? 'Zapisywanie...' : 'Zapisz rozgrywkę'}
              </button>
              <button type="button" className="btn-cancel" onClick={() => { setSessionFormOpen(false); setSessionName(''); setNotes(''); setScores([]) }}>
                Anuluj
              </button>
            </div>
          </form>
        )}

        {sessions.length === 0 ? (
          <p className="status small">Brak rozgrywek</p>
        ) : (
          <ul className="session-history">
            {sessions.map(s => (
              <li key={s.id} className="session-history-item">
                {editingSessionId === s.id ? (
                  <form className="session-edit-form" onSubmit={handleSessionEdit}>
                    <input
                      type="text"
                      value={editSessionName}
                      onChange={e => setEditSessionName(e.target.value)}
                      placeholder="Nazwa rozgrywki"
                      className="session-notes-input"
                    />
                    <input
                      type="text"
                      value={editSessionNotes}
                      onChange={e => setEditSessionNotes(e.target.value)}
                      placeholder="Notatki"
                      className="session-notes-input"
                      style={{ marginTop: '0.4rem' }}
                    />
                    <div className="form-row" style={{ marginTop: '0.4rem' }}>
                      <button type="submit" disabled={sessionEditSaving}>{sessionEditSaving ? '...' : 'Zapisz'}</button>
                      <button type="button" className="btn-cancel" onClick={() => setEditingSessionId(null)}>Anuluj</button>
                    </div>
                  </form>
                ) : (
                  <>
                    <div className="session-history-date">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span className="session-name">{s.name ?? `Rozgrywka#${sessions.length - sessions.indexOf(s)}`}</span>
                        <button className="btn-edit-inline" onClick={() => openSessionEdit(s)} title="Edytuj">✎</button>
                      </div>
                      <span className="session-date-sub">{s.played_at}</span>
                    </div>
                    {s.notes && <p className="session-notes">{s.notes}</p>}
                    {s.scores.length > 0 && (
                      <ul className="score-list">
                        {s.scores.map(score => (
                          <li key={score.id} className={`score-item${score.winner ? ' winner' : ''}`}>
                            <span>{score.player.name}</span>
                            {score.points != null && <span>{score.points} pkt</span>}
                            {score.winner && <span className="winner-badge">Zwycięzca</span>}
                          </li>
                        ))}
                      </ul>
                    )}
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
