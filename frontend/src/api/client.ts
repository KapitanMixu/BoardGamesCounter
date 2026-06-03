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

export interface Game {
  id: number
  name: string
  min_players: number
  max_players: number
  times_played: number
  last_played_at: string | null
}

export const api = {
  games: {
    list: () => request<Game[]>('/games/'),
  },
}
