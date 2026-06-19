import { type FormEvent, useState } from 'react'
import { login, register } from '../api/client'

interface Props {
  onLogin: () => void
}

export default function LoginForm({ onLogin }: Props) {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [inviteCode, setInviteCode] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      if (mode === 'login') {
        await login(username, password)
      } else {
        await register(username, password, inviteCode)
      }
      onLogin()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd')
    } finally {
      setLoading(false)
    }
  }

  function switchMode(next: 'login' | 'register') {
    setMode(next)
    setError(null)
  }

  return (
    <div className="login-wrapper">
      <h1>Board Games Counter</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab${mode === 'login' ? ' active' : ''}`}
            onClick={() => switchMode('login')}
          >Logowanie</button>
          <button
            type="button"
            className={`auth-tab${mode === 'register' ? ' active' : ''}`}
            onClick={() => switchMode('register')}
          >Rejestracja</button>
        </div>
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
        {mode === 'register' && (
          <label>
            Kod zaproszenia
            <input
              type="text"
              value={inviteCode}
              onChange={e => setInviteCode(e.target.value)}
              placeholder="kod od admina"
              required
            />
          </label>
        )}
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? '...' : mode === 'login' ? 'Zaloguj' : 'Załóż konto'}
        </button>
        {mode === 'register' && (
          <p className="auth-hint">Konto znajomego = tylko podgląd. Edycja zarezerwowana dla admina.</p>
        )}
      </form>
    </div>
  )
}
