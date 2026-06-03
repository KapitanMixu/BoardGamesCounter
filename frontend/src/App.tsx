import { useState } from 'react'
import { clearToken, getToken } from './api/client'
import LoginForm from './components/LoginForm'
import GameList from './components/GameList'
import './App.css'

export default function App() {
  const [loggedIn, setLoggedIn] = useState(() => getToken() !== null)

  function handleLogout() {
    clearToken()
    setLoggedIn(false)
  }

  if (!loggedIn) {
    return <LoginForm onLogin={() => setLoggedIn(true)} />
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Board Games Counter</h1>
        <button className="logout-btn" onClick={handleLogout}>Wyloguj</button>
      </header>
      <main>
        <GameList />
      </main>
    </div>
  )
}
