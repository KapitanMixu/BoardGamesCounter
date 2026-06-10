import { type FormEvent, useState } from 'react'
import { login, setToken } from '../api/client'

interface Props {
  onLogin: () => void
}

export default function LoginForm({ onLogin }: Props) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const token = await login(username, password)
      setToken(token)
      onLogin()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd logowania')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrapper">
      <h1>Board Games Counter</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Logowanie</h2>
        <label>
          Użytkownik
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            autoFocus
            required
          />
        </label>
        <label>
          Hasło
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? 'Logowanie...' : 'Zaloguj'}
        </button>
      </form>
    </div>
  )
}
