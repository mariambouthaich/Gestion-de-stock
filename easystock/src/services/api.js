import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// Normalize: strip trailing /api to avoid double /api/api
const baseURL = API_BASE.replace(/\/api\/?$/, '')

export const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
})

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}

// ── Request interceptor: auto-inject token ────────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('es_access_token')
  if (token && !config.headers['Authorization']) {
    config.headers['Authorization'] = `JWT ${token}`
  }
  return config
})

// ── Response interceptor: normalize errors ───────────────────────────────
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err?.response?.status
    const data   = err?.response?.data

    // Build a readable message
    let message = 'Erreur réseau'
    if (data) {
      if (typeof data === 'string') message = data
      else if (data.detail)  message = data.detail
      else if (data.error)   message = data.error
      else if (data.message) message = data.message
      else if (data.non_field_errors) message = data.non_field_errors[0]
      else {
        // Collect field errors
        const parts = Object.entries(data)
          .filter(([, v]) => v)
          .map(([k, v]) => `${k}: ${Array.isArray(v) ? v[0] : v}`)
        if (parts.length) message = parts.join(' | ')
      }
    } else if (status) {
      message = `Erreur ${status}`
    } else if (err.message) {
      message = err.message
    }

    return Promise.reject({ status, data, message, original: err })
  }
)

// Ensure trailing slash for Django's APPEND_SLASH
export function url(path) {
  const [base, qs = ''] = path.split('?')
  const fixed = base.endsWith('/') ? base : `${base}/`
  return qs ? `${fixed}?${qs}` : fixed
}
