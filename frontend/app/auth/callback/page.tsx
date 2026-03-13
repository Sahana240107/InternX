'use client'

import { useEffect, useRef } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useAuthStore } from '@/lib/store/authStore'
import api from '@/lib/api'

// This page is where GitHub redirects after the user approves the login.
// URL will look like: /auth/callback?code=abc123
// We take that 'code', send it to our backend, and get back our JWT.

export default function CallbackPage() {
  const router      = useRouter()
  const params      = useSearchParams()
  const setAuth     = useAuthStore((s) => s.setAuth)
  const called      = useRef(false)  // prevent double-call in React strict mode

  useEffect(() => {
    const code = params.get('code')

    // GitHub sometimes sends an error instead of a code
    const error = params.get('error')
    if (error) {
      router.replace(`/auth/login?error=${error}`)
      return
    }

    if (!code || called.current) return
    called.current = true

    const exchange = async () => {
      try {
        // Send the code to our FastAPI backend
        // Backend exchanges it with GitHub (server-to-server) and returns our JWT
        const { data } = await api.post('/api/auth/github/callback', { code })

        // Save user + token to global Zustand store (also persisted in localStorage)
        setAuth(data.user, data.access_token)

        // Redirect based on role:
        // New interns who haven't set their intern_role yet go to onboarding
        if (data.user.role === 'intern' && !data.user.intern_role) {
          router.replace('/auth/onboarding')
        } else {
          router.replace('/dashboard')
        }

      } catch (err: any) {
        console.error('Auth callback error:', err)
        router.replace('/auth/login?error=auth_failed')
      }
    }

    exchange()
  }, [params])

  return (
    <main className="min-h-screen flex items-center justify-center bg-indigo-50">
      <div className="text-center space-y-4">
        {/* Spinner */}
        <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mx-auto" />
        <p className="text-gray-600 font-medium">Signing you in...</p>
        <p className="text-gray-400 text-sm">Connecting your GitHub account</p>
      </div>
    </main>
  )
}
