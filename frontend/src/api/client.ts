const BASE = '/api/v1'

export function getToken(): string | null {
  return localStorage.getItem('token')
}

export function setToken(token: string): void {
  localStorage.setItem('token', token)
}

export function clearToken(): void {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('username')
  localStorage.removeItem('player_id')
}

export function getPlayerId(): number | null {
  const v = localStorage.getItem('player_id')
  return v !== null && v !== 'null' ? Number(v) : null
}

export function getRole(): string | null {
  return localStorage.getItem('role')
}

export function isAdmin(): boolean {
  return localStorage.getItem('role') === 'admin'
}

export function getUsername(): string | null {
  return localStorage.getItem('username')
}

interface AuthResponse {
  access_token: string
  role: string
  username: string
  player_id: number | null
}

function storeAuth(data: AuthResponse): void {
  setToken(data.access_token)
  localStorage.setItem('role', data.role)
  localStorage.setItem('username', data.username)
  localStorage.setItem('player_id', String(data.player_id ?? null))
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getToken()
  const res = await fetch(BASE + path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  })
  if (res.status === 401) {
    clearToken()
    throw new Error('Unauthorized')
  }
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

export async function login(username: string, password: string): Promise<void> {
  const body = new URLSearchParams({ username, password })
  const res = await fetch('/auth/token', { method: 'POST', body })
  if (!res.ok) throw new Error('Nieprawidłowe dane logowania')
  storeAuth(await res.json())
}

export async function register(username: string, password: string, inviteCode: string): Promise<void> {
  const res = await fetch('/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, invite_code: inviteCode }),
  })
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new Error(data.detail ?? 'Rejestracja nie powiodła się')
  }
  storeAuth(await res.json())
}

export async function linkPlayer(option: { player_id: number } | { player_name: string }): Promise<void> {
  const res = await fetch('/auth/link-player', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}` },
    body: JSON.stringify(option),
  })
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new Error(data.detail ?? 'Nie udało się powiązać gracza')
  }
  const { player_id } = await res.json()
  localStorage.setItem('player_id', String(player_id))
}

export type DurationType = 'total' | 'per_player'

export interface Game {
  id: number
  name: string
  min_players: number
  max_players: number
  duration_minutes: number | null
  duration_type: DurationType | null
  bgg_url: string | null
  thumbnail_url: string | null
  times_played: number
  last_played_at: string | null
}

export interface GameCreate {
  name: string
  min_players: number
  max_players: number
  duration_minutes?: number | null
  duration_type?: DurationType | null
  bgg_url?: string | null
}

export interface GameUpdate {
  name?: string
  min_players?: number
  max_players?: number
  duration_minutes?: number | null
  duration_type?: DurationType | null
  bgg_url?: string | null
}

export interface Player {
  id: number
  name: string
  total_plays: number
  total_wins: number
}

export interface PlayerCreate {
  name: string
}

export interface PlayerGameStat {
  game_id: number
  game_name: string
  plays: number
  wins: number
}

export interface PlayerSessionHistoryItem {
  session_id: number
  game_id: number
  game_name: string
  session_name: string | null
  played_at: string
  points: number | null
  winner: boolean
}

export interface PlayerStats {
  id: number
  name: string
  total_plays: number
  total_wins: number
  top_games: PlayerGameStat[]
  session_history: PlayerSessionHistoryItem[]
}

export interface Score {
  id: number
  player: Player
  points: number | null
  winner: boolean
}

export interface ScoreCreate {
  player_id: number
  points?: number | null
  winner?: boolean
}

export interface GameSession {
  id: number
  game_id: number
  name: string | null
  played_at: string
  notes: string | null
  scores: Score[]
}

export interface GameSessionCreate {
  game_id: number
  name?: string | null
  notes?: string | null
  scores?: ScoreCreate[]
}

export interface GameSessionUpdate {
  name?: string | null
  notes?: string | null
}

export interface WishlistItem {
  id: number
  name: string
  planszeo_url: string | null
  bgg_url: string | null
  notes: string | null
  best_price: number | null
  best_price_shop: string | null
  offer_count: number | null
  price_updated_at: string | null
  created_at: string
}

export interface WishlistItemCreate {
  name: string
  planszeo_url?: string | null
  bgg_url?: string | null
  notes?: string | null
}

export interface WishlistItemUpdate {
  name?: string
  planszeo_url?: string | null
  bgg_url?: string | null
  notes?: string | null
}

export interface Expansion {
  id: number
  name: string
}

export interface ExpansionCreate {
  name: string
}

export interface ExpansionUpdate {
  name?: string
}

export interface BggResult {
  id: string
  name: string
  year: string | null
  url: string
}

export const api = {
  games: {
    list: () => request<Game[]>('/games/'),
    get: (id: number) => request<Game>(`/games/${id}`),
    create: (data: GameCreate) => request<Game>('/games/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id: number, data: GameUpdate) => request<Game>(`/games/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    sessions: (id: number) => request<GameSession[]>(`/games/${id}/sessions/`),
  },
  players: {
    list: () => request<Player[]>('/players/'),
    get: (id: number) => request<Player>(`/players/${id}`),
    stats: (id: number) => request<PlayerStats>(`/players/${id}/stats`),
    create: (data: PlayerCreate) => request<Player>('/players/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },
  sessions: {
    list: () => request<GameSession[]>('/sessions/'),
    get: (id: number) => request<GameSession>(`/sessions/${id}`),
    create: (data: GameSessionCreate) => request<GameSession>('/sessions/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id: number, data: GameSessionUpdate) => request<GameSession>(`/sessions/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    delete: (id: number) => request<void>(`/sessions/${id}`, { method: 'DELETE' }),
  },
  bgg: {
    search: (q: string) => request<BggResult[]>(`/bgg/search?q=${encodeURIComponent(q)}`),
  },
  wishlist: {
    list: () => request<WishlistItem[]>('/wishlist/'),
    create: (data: WishlistItemCreate) => request<WishlistItem>('/wishlist/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id: number, data: WishlistItemUpdate) => request<WishlistItem>(`/wishlist/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    delete: (id: number) => request<void>(`/wishlist/${id}`, { method: 'DELETE' }),
    refreshPrice: (id: number) => request<WishlistItem>(`/wishlist/${id}/refresh-price`, { method: 'POST' }),
  },
  expansions: {
    list: (gameId: number) => request<Expansion[]>(`/games/${gameId}/expansions/`),
    create: (gameId: number, data: ExpansionCreate) => request<Expansion>(`/games/${gameId}/expansions/`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (gameId: number, expansionId: number, data: ExpansionUpdate) => request<Expansion>(`/games/${gameId}/expansions/${expansionId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    delete: (gameId: number, expansionId: number) => request<void>(`/games/${gameId}/expansions/${expansionId}`, {
      method: 'DELETE',
    }),
  },
}
