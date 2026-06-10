import { useEffect, useState } from 'react'
import { api, type GameSession } from '../api/client'

export default function SessionList() {
  const [sessions, setSessions] = useState<GameSession[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.sessions.list()
      .then(setSessions)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>

  return (
    <section className="session-list">
      <h2>Sesje ({sessions.length})</h2>
      <ul>
        {sessions.map(session => (
          <li key={session.id} className="session-card">
            <div className="session-header">
              <span className="session-game">Gra #{session.game_id}</span>
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
