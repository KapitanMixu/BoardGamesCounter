import { useEffect, useState } from 'react'
import { api, type Game } from '../api/client'

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
      <h2>Gry ({games.length})</h2>
      <ul>
        {games.map(game => (
          <li key={game.id} className="game-card">
            <div className="game-name">{game.name}</div>
            <div className="game-meta">
              <span>{game.min_players}–{game.max_players} graczy</span>
              <span>{game.times_played} {game.times_played === 1 ? 'sesja' : 'sesje'}</span>
              <span>{game.last_played_at ?? 'nigdy nie grane'}</span>
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}
