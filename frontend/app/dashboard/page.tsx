'use client'

import { useAuthStore } from '@/lib/store/authStore'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DashboardPage() {
  const { user, clearAuth } = useAuthStore()
  const router = useRouter()

  useEffect(() => {
    if (!user) router.replace('/auth/login')
  }, [user])

  const handleLogout = () => {
    clearAuth()
    router.replace('/auth/login')
  }

  if (!user) return null

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            {user.avatar_url && (
              <img src={user.avatar_url} alt={user.name} className="w-12 h-12 rounded-full" />
            )}
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Welcome back, {user.name.split(' ')[0]}!</h1>
              <p className="text-gray-500 text-sm capitalize">{user.role} · {user.intern_role || 'No role set'}</p>
            </div>
          </div>
          <button onClick={handleLogout} className="text-sm text-gray-500 hover:text-red-500 transition-colors">
            Logout
          </button>
        </div>

        {/* Auth success card */}
        <div className="bg-white rounded-xl border border-green-200 bg-green-50 p-6">
          <h2 className="text-green-800 font-semibold text-lg">✅ Module 1 Complete — Auth is working!</h2>
          <p className="text-green-700 text-sm mt-1">
            You are logged in as <strong>{user.email}</strong> with role <strong>{user.role}</strong>.
          </p>
          <p className="text-green-600 text-sm mt-3">
            Next: Module 2 will build the full dashboard with tasks and sprint boards here.
          </p>
        </div>

        {/* User details */}
        <div className="mt-6 bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-700 mb-3">Your profile data</h3>
          <pre className="text-xs text-gray-500 bg-gray-50 p-4 rounded-lg overflow-auto">
            {JSON.stringify(user, null, 2)}
          </pre>
        </div>

      </div>
    </main>
  )
}
