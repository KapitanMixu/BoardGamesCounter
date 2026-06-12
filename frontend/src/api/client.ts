const BASE = '/api/v1'

export function getToken(): string | null {
  return localStorage.getItem('token')
}

export function setToken(token: string): void {
  localStorage.setItem('token', token)
}

export function clearToken(): void {
  localStorage.removeItem('token')
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

export async function login(username: string, password: string): Promise<string> {
  const body = new URLSearchParams({ username, password })
  const res = await fetch('/auth/token', { method: 'POST', body })
  if (!res.ok) throw new Error('Nieprawidłowe dane logowania')
  const data = await res.json()
  return data.access_token
}

export type DurationType = 'total' | 'per_player'

export interface Game {
  id: number
  name: string
  min_players: number
  max_players: number
  duration_minutes: number | null
  duration_type: DurationType | null
  times_played: number
  last_played_at: string | null
}

export interface GameCreate {
  name: string
  min_players: number
  max_players: number
  duration_minutes?: number | null
  duration_type?: DurationType | null
}

export interface GameUpdate {
  name?: string
  min_players?: number
  max_players?: number
  duration_minutes?: number | null
  duration_type?: DurationType | null
}

export interface Player {
  id: number
  name: string
}

export interface PlayerCreate {
  name: string
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
