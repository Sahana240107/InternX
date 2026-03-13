'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store/authStore'

export default function LoginPage() {
  const router    = useRouter()
  const isLoggedIn = useAuthStore((s) => s.isLoggedIn)

  // If already logged in, skip the login page entirely
  useEffect(() => {
    if (isLoggedIn()) router.replace('/dashboard')
  }, [])

  const handleGitHubLogin = () => {
    // Redirect to GitHub's OAuth page
    // GitHub will redirect back to /auth/callback with a one-time code
    const params = new URLSearchParams({
      client_id: process.env.NEXT_PUBLIC_GITHUB_CLIENT_ID!,
      scope:     'user:email read:user',
      redirect_uri: `${window.location.origin}/auth/callback`,
    })
    window.location.href = `https://github.com/login/oauth/authorize?${params}`
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="w-full max-w-md mx-auto px-6">

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-10 text-center">

          {/* Logo */}
          <div className="mb-6">
            <span className="text-4xl font-bold text-indigo-600">InternX</span>
            <p className="mt-2 text-gray-500 text-sm">AI-Powered Virtual Internship Simulator</p>
          </div>

          {/* Divider */}
          <div className="my-8 border-t border-gray-100" />

          {/* Value props */}
          <div className="space-y-3 text-left mb-8">
            {[
              '🎯  Role-based internship simulation',
              '🤖  AI mentor with real-time feedback',
              '📁  GitHub portfolio auto-generated',
              '🏆  Verified skill certificates',
            ].map((item) => (
              <p key={item} className="text-sm text-gray-600">{item}</p>
            ))}
          </div>

          {/* GitHub login button */}
          <button
            onClick={handleGitHubLogin}
            className="w-full flex items-center justify-center gap-3 bg-gray-900 hover:bg-gray-800 text-white font-medium py-3 px-6 rounded-xl transition-colors duration-200"
          >
            {/* GitHub SVG icon */}
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
            Continue with GitHub
          </button>

          <p className="mt-4 text-xs text-gray-400">
            By signing in you agree to use this platform for learning purposes.
          </p>
        </div>
      </div>
    </main>
  )
}
