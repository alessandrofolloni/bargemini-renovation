import axios from 'axios'

// Single source of truth for the backend URL. Override at build/run time with
// VITE_API_URL (e.g. in production); falls back to the local dev server.
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL })

// Attach the staff token to every request when present.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default api
