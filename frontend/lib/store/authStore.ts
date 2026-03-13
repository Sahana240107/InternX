import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// This is the global auth state — any component can read from it
// 'persist' saves it to localStorage so the user stays logged in on refresh

interface User {
  id: string
  email: string
  name: string
  avatar_url?: string
  github_username?: string
  role: 'intern' | 'mentor' | 'admin'
  intern_role?: string
  bio?: string
}

interface AuthStore {
  user:     User | null
  token:    string | null
  setAuth:  (user: User, token: string) => void
  clearAuth: () => void
  isLoggedIn: () => boolean
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user:  null,
      token: null,

      setAuth: (user, token) => set({ user, token }),

      clearAuth: () => set({ user: null, token: null }),

      // Helper — components call this instead of checking user !== null
      isLoggedIn: () => get().token !== null && get().user !== null,
    }),
    {
      name: 'internx-auth',   // localStorage key name
    }
  )
)
