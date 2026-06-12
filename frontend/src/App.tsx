import { useState } from 'react'
import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom'
import { clearToken, getToken } from './api/client'
import LoginForm from './components/LoginForm'
import GameList from './components/GameList'
import GameDetail from './components/GameDetail'
import PlayerList from './components/PlayerList'
import SessionList from './components/SessionList'
import SessionDetail from './components/SessionDetail'
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
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Board Games Counter</h1>
          <nav className="app-nav">
            <NavLink to="/games" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Gry</NavLink>
            <NavLink to="/players" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Gracze</NavLink>
            <NavLink to="/sessions" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Sesje</NavLink>
          </nav>
          <button className="logout-btn" onClick={handleLogout}>Wyloguj</button>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/games" replace />} />
            <Route path="/games" element={<GameList />} />
            <Route path="/games/:id" element={<GameDetail />} />
            <Route path="/players" element={<PlayerList />} />
            <Route path="/sessions" element={<SessionList />} />
            <Route path="/sessions/:id" element={<SessionDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
