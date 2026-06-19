import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { api, isAdmin, type GameSession, type Game } from '../api/client'

export default function SessionDetail() {
  const { id } = useParams<{ id: string }>()
  const sessionId = Number(id)
  const navigate = useNavigate()

  const [session, setSession] = useState<GameSession | null>(null)
  const [game, setGame] = useState<Game | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [editOpen, setEditOpen] = useState(false)
  const [editName, setEditName] = useState('')
  const [editNotes, setEditNotes] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    api.sessions.get(sessionId)
      .then(async s => {
        setSession(s)
        const g = await api.games.get(s.game_id)
        setGame(g)
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [sessionId])

  function openEdit() {
    if (!session) return
    setEditName(session.name ?? '')
    setEditNotes(session.notes ?? '')
    setEditOpen(true)
  }

  async function handleEdit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    try {
      const updated = await api.sessions.update(sessionId, {
        name: editName.trim() || null,
        notes: editNotes.trim() || null,
      })
      setSession(updated)
      setEditOpen(false)
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!confirm('Usunąć tę sesję?')) return
    await api.sessions.delete(sessionId)
    navigate('/sessions')
  }

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>
  if (!session) return <p className="status error">Nie znaleziono sesji</p>

  return (
    <section className="game-detail">
      <Link to="/sessions" className="back-link">← Wróć do sesji</Link>

      <div className="detail-header">
        {editOpen ? (
          <form className="game-edit-form" onSubmit={handleEdit}>
            <div className="form-row">
              <input
                type="text"
                value={editName}
                onChange={e => setEditName(e.target.value)}
                placeholder="Nazwa sesji"
                className="session-notes-input"
              />
            </div>
            <div className="form-row" style={{ marginTop: '0.5rem' }}>
              <input
                type="text"
                value={editNotes}
                onChange={e => setEditNotes(e.target.value)}
                placeholder="Notatki"
                className="session-notes-input"
              />
            </div>
            <div className="form-row" style={{ marginTop: '0.5rem' }}>
              <button type="submit" disabled={saving}>{saving ? 'Zapisywanie...' : 'Zapisz'}</button>
              <button type="button" className="btn-cancel" onClick={() => setEditOpen(false)}>Anuluj</button>
            </div>
          </form>
        ) : (
          <>
            <div className="session-detail-head">
              {game?.thumbnail_url
                ? <img src={game.thumbnail_url} alt="" className="game-thumb game-thumb-lg" />
                : <span className="game-thumb game-thumb-lg game-thumb-placeholder">{(game?.name ?? '?').charAt(0).toUpperCase()}</span>}
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <h2 style={{ marginBottom: '0.4rem' }}>{session.name ?? `Sesja #${session.id}`}</h2>
                  {isAdmin() && <button className="btn-edit-inline" onClick={openEdit} title="Edytuj">✎</button>}
                </div>
                <div className="game-meta">
                  {game
                    ? <Link to={`/games/${game.id}`} className="game-chip">🎲 {game.name}</Link>
                    : <span className="game-chip">🎲 Gra #{session.game_id}</span>}
                  <span>📅 {new Date(session.played_at).toLocaleDateString('pl-PL')}</span>
                </div>
              </div>
            </div>
            {session.notes && <p className="session-notes" style={{ marginTop: '0.75rem' }}>{session.notes}</p>}
          </>
        )}
      </div>

      {session.scores.length > 0 && (
        <div className="detail-card">
          <h3>Wyniki</h3>
          <ul className="score-list" style={{ marginTop: '0.5rem' }}>
            {session.scores
              .slice()
              .sort((a, b) => (b.points ?? 0) - (a.points ?? 0))
              .map(score => (
                <li key={score.id} className={`score-item${score.winner ? ' winner' : ''}`}>
                  <Link to={`/players/${score.player.id}`} className="bar-label">{score.player.name}</Link>
                  {score.points != null && <span>{score.points} pkt</span>}
                  {score.winner && <span className="winner-crown" title="Zwycięzca">👑</span>}
                </li>
              ))}
          </ul>
        </div>
      )}

      {isAdmin() && (
        <div style={{ marginTop: '1.5rem' }}>
          <button className="btn-danger" onClick={handleDelete}>
            Usuń sesję
          </button>
        </div>
      )}
    </section>
  )
}
