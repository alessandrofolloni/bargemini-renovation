import axios from 'axios'

// Single source of truth for the backend URL.
//  - dev: the separate Vite server talks to the backend on :8000
//  - prod build: relative URLs, so the backend that serves the built site
//    also answers the API (single origin — works behind one tunnel/host)
// Override either with VITE_API_URL when you need a custom backend address.
const baseURL = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? 'http://localhost:8000' : '')

const api = axios.create({ baseURL })

// Attach the staff token to every request when present.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default api
