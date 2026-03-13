import axios from 'axios'
import { useAuthStore } from '@/lib/store/authStore'

// One axios instance for the whole app — base URL set once here
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor — automatically adds the JWT token to every request
// So every component just calls api.get('/api/...') without worrying about auth headers
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor — if the server returns 401 (token expired), log the user out
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().clearAuth()
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

export default api
