import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api, type PlayerStats } from '../api/client'

export default function PlayerDetail() {
  const { id } = useParams<{ id: string }>()
  const playerId = Number(id)

  const [stats, setStats] = useState<PlayerStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api.players.stats(playerId)
      .then(setStats)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [playerId])

  if (loading) return <p className="status">Ładowanie...</p>
  if (error) return <p className="status error">Błąd: {error}</p>
  if (!stats) return <p className="status error">Nie znaleziono gracza</p>

  const winrate = stats.total_plays > 0
    ? Math.round((stats.total_wins / stats.total_plays) * 100)
    : 0
  const maxPlays = stats.top_games.reduce((m, g) => Math.max(m, g.plays), 0)

  return (
    <section className="game-detail">
      <Link to="/players" className="back-link">← Wróć do listy</Link>

      <div className="detail-header">
        <h2>{stats.name}</h2>
        <div className="game-meta">
          <span>{stats.total_plays} rozgrywek</span>
          <span>{stats.total_wins} wygranych</span>
          <span>{winrate}% winrate</span>
        </div>
      </div>

      {/* Ogólny winrate — donut */}
      <div className="detail-card">
        <h3>Ogólny winrate</h3>
        <div className="winrate-overview">
          <div
            className="winrate-donut"
            style={{ background: `conic-gradient(var(--color-primary) ${winrate * 3.6}deg, var(--color-surface-2) 0deg)` }}
          >
            <div className="winrate-donut-hole">
              <span className="winrate-pct">{winrate}%</span>
            </div>
          </div>
          <div className="winrate-legend">
            <div><span className="legend-dot win" /> Wygrane: {stats.total_wins}</div>
            <div><span className="legend-dot loss" /> Przegrane: {stats.total_plays - stats.total_wins}</div>
          </div>
        </div>
      </div>

      {/* Top 10 gier — bary */}
      <div className="detail-card">
        <h3>Top gry (najczęściej grane)</h3>
        {stats.top_games.length === 0 ? (
          <p className="status small">Brak rozgrywek</p>
        ) : (
          <ul className="bar-chart">
            {stats.top_games.map(g => {
              const gameWinrate = g.plays > 0 ? Math.round((g.wins / g.plays) * 100) : 0
              return (
                <li key={g.game_id} className="bar-row">
                  <Link to={`/games/${g.game_id}`} className="bar-label">{g.game_name}</Link>
                  <div className="bar-track">
                    <div
                      className="bar-fill"
                      style={{ width: `${maxPlays > 0 ? (g.plays / maxPlays) * 100 : 0}%` }}
                    >
                      <div
                        className="bar-fill-wins"
                        style={{ width: `${g.plays > 0 ? (g.wins / g.plays) * 100 : 0}%` }}
                      />
                    </div>
                  </div>
                  <span className="bar-value">{g.plays}× · {gameWinrate}% W</span>
                </li>
              )
            })}
          </ul>
        )}
        {stats.top_games.length > 0 && (
          <div className="bar-chart-legend">
            <span><span className="legend-dot win" /> wygrane</span>
            <span><span className="legend-dot plays" /> rozgrywki</span>
          </div>
        )}
      </div>

      {/* Historia sesji */}
      <div className="detail-card">
        <h3>Historia rozgrywek ({stats.session_history.length})</h3>
        {stats.session_history.length === 0 ? (
          <p className="status small">Brak rozgrywek</p>
        ) : (
          <ul className="session-history">
            {stats.session_history.map(h => (
              <li key={h.session_id} className="session-history-item">
                <div className="session-history-date">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Link to={`/sessions/${h.session_id}`} className="session-name">
                      {h.session_name ?? `Rozgrywka #${h.session_id}`}
                    </Link>
                    {h.winner && <span className="winner-crown" title="Zwycięzca">👑</span>}
                  </div>
                  <span className="session-date-sub">{new Date(h.played_at).toLocaleString('pl-PL')}</span>
                </div>
                <p className="session-notes">
                  <Link to={`/games/${h.game_id}`} className="bgg-link" style={{ border: 'none', padding: 0 }}>
                    {h.game_name}
                  </Link>
                  {h.points != null && <span style={{ marginLeft: '0.75rem' }}>{h.points} pkt</span>}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
