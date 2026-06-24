import { api, setAuthToken } from './api'

const TOKEN_KEY = 'es_access_token'
const USER_KEY  = 'es_user'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getUser() {
  try { return JSON.parse(localStorage.getItem(USER_KEY) || 'null') } catch { return null }
}

export function isAuthenticated() {
  return Boolean(getToken())
}

export async function login({ username, password }) {
  const endpoint = import.meta.env.VITE_AUTH_ENDPOINT || '/api/login/'
  const ep = endpoint.endsWith('/') ? endpoint : `${endpoint}/`

  const res = await api.post(ep, { username, password })
  const d = res.data

  const token = d.access || d.access_token || d.token || d.jwt
  if (!token) throw new Error('Token manquant dans la réponse')

  localStorage.setItem(TOKEN_KEY, token)
  if (d.refresh) localStorage.setItem('es_refresh_token', d.refresh)
  localStorage.setItem(USER_KEY, JSON.stringify({
    username: d.username || username,
    email: d.email || '',
    is_staff: d.is_staff || false,
  }))

  // Essaie JWT d'abord (simplejwt par défaut), sinon Bearer
  setAuthToken(token, 'JWT')
  return d
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem('es_refresh_token')
  localStorage.removeItem(USER_KEY)
  setAuthToken(null)
}

// Restore token on load avec préfixe JWT
const _token = getToken()
if (_token) setAuthToken(_token, 'JWT')