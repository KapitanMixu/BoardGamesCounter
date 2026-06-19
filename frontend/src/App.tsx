import { useState } from 'react'
import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom'
import { clearToken, getPlayerId, getToken, getUsername, isAdmin } from './api/client'
import LoginForm from './components/LoginForm'
import PlayerPicker from './components/PlayerPicker'
import GameList from './components/GameList'
import GameDetail from './components/GameDetail'
import PlayerList from './components/PlayerList'
import PlayerDetail from './components/PlayerDetail'
import SessionList from './components/SessionList'
import SessionDetail from './components/SessionDetail'
import Wishlist from './components/Wishlist'
import './App.css'

export default function App() {
  const [loggedIn, setLoggedIn] = useState(() => getToken() !== null)
  const [playerLinked, setPlayerLinked] = useState(() => getPlayerId() !== null || isAdmin())

  function handleLogout() {
    clearToken()
    setLoggedIn(false)
    setPlayerLinked(false)
  }

  function handleLogin() {
    setLoggedIn(true)
    setPlayerLinked(getPlayerId() !== null || isAdmin())
  }

  if (!loggedIn) {
    return <LoginForm onLogin={handleLogin} />
  }

  if (!playerLinked) {
    return <PlayerPicker onLinked={() => setPlayerLinked(true)} />
  }

  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Gry Mixa</h1>
          <nav className="app-nav">
            <NavLink to="/games" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Gry</NavLink>
            <NavLink to="/players" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Gracze</NavLink>
            <NavLink to="/sessions" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Sesje</NavLink>
            <NavLink to="/wishlist" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>Lista życzeń</NavLink>
          </nav>
          <span className="user-badge">
            <strong>{getUsername()}</strong>
            <span className="role-pill">{isAdmin() ? 'admin' : 'podgląd'}</span>
          </span>
          <button className="logout-btn" onClick={handleLogout}>Wyloguj</button>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/games" replace />} />
            <Route path="/games" element={<GameList />} />
            <Route path="/games/:id" element={<GameDetail />} />
            <Route path="/players" element={<PlayerList />} />
            <Route path="/players/:id" element={<PlayerDetail />} />
            <Route path="/sessions" element={<SessionList />} />
            <Route path="/sessions/:id" element={<SessionDetail />} />
            <Route path="/wishlist" element={<Wishlist />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
