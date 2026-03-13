'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store/authStore'
import api from '@/lib/api'
import { toast } from 'sonner'

const roles = [
  { id: 'frontend',  title: 'Frontend',  icon: '⚡', description: 'React, JavaScript, CSS, UI/UX', color: '#5b4fff', bg: '#ede9ff' },
  { id: 'backend',   title: 'Backend',   icon: '⚙️', description: 'APIs, databases, system design', color: '#3b82f6', bg: '#eff6ff' },
  { id: 'fullstack', title: 'Full Stack', icon: '🔥', description: 'End-to-end product development', color: '#f59e0b', bg: '#fffbeb' },
  { id: 'devops',    title: 'DevOps',    icon: '🚀', description: 'CI/CD, cloud, infrastructure',   color: '#00c896', bg: '#e0fff7' },
  { id: 'design',    title: 'Design',    icon: '✦',  description: 'Figma, design systems, UX research', color: '#ec4899', bg: '#fdf2f8' },
]

export default function OnboardingPage() {
  const [selected, setSelected] = useState(null)
  const [loading, setLoading]   = useState(false)
  const router = useRouter()
  const { user, token, setAuth } = useAuthStore()

  const handleSubmit = async () => {
  if (!selected) return
  setLoading(true)
  try {
    await api.put('/api/auth/me', { intern_role: selected })
    setAuth({ ...user, intern_role: selected }, token)
    // Set cookie manually before redirect
    document.cookie = `internx-token=${token}; path=/; max-age=604800; SameSite=Lax`
    toast.success('Welcome to InternX! 🎉')
    setTimeout(() => {
      window.location.href = '/dashboard'
    }, 500)
  } catch {
    toast.error('Something went wrong')
  } finally {
    setLoading(false)
  }
}
  return (
    <div className="min-h-screen flex items-center justify-center p-6" style={{ background: 'var(--surface)' }}>
      <div className="fixed top-0 right-0 w-96 h-96 rounded-full pointer-events-none"
        style={{ background: 'radial-gradient(circle, rgba(91,79,255,0.06) 0%, transparent 70%)', filter: 'blur(60px)' }} />

      <div className="w-full max-w-2xl animate-fade-up">
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-4"
            style={{ background: 'var(--accent-soft)', color: 'var(--accent)', border: '1px solid rgba(91,79,255,0.2)' }}>
            Step 1 of 1
          </div>
          <h1 className="text-4xl font-display mb-3" style={{ color: 'var(--ink)' }}>Choose your track</h1>
          <p style={{ color: 'var(--ink-muted)' }}>This shapes your tasks, AI mentor, and portfolio focus</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
          {roles.map((role, i) => (
            <button key={role.id} onClick={() => setSelected(role.id)}
              className="p-5 rounded-2xl text-left transition-all duration-200 animate-fade-up"
              style={{
                animationDelay: `${i * 0.07}s`,
                opacity: 0,
                background: selected === role.id ? role.bg : 'white',
                border: selected === role.id ? `2px solid ${role.color}` : '2px solid var(--border)',
                transform: selected === role.id ? 'scale(1.02)' : 'scale(1)',
                boxShadow: selected === role.id ? `0 8px 24px ${role.color}20` : '0 1px 3px rgba(0,0,0,0.04)',
              }}>
              <div className="text-2xl mb-3">{role.icon}</div>
              <div className="font-display font-bold text-base mb-1"
                style={{ color: selected === role.id ? role.color : 'var(--ink)' }}>
                {role.title}
              </div>
              <div className="text-xs leading-relaxed" style={{ color: 'var(--ink-muted)' }}>
                {role.description}
              </div>
              {selected === role.id && (
                <div className="mt-3 flex items-center gap-1">
                  <div className="w-4 h-4 rounded-full flex items-center justify-center" style={{ background: role.color }}>
                    <svg className="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <span className="text-xs font-semibold" style={{ color: role.color }}>Selected</span>
                </div>
              )}
            </button>
          ))}
        </div>

        <div className="flex justify-center">
          <button onClick={handleSubmit} disabled={!selected || loading}
            className="btn-primary px-10 py-4 text-base"
            style={{ opacity: (!selected || loading) ? 0.4 : 1, cursor: (!selected || loading) ? 'not-allowed' : 'pointer' }}>
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                Setting up...
              </span>
            ) : (
              <>Start My Internship →</>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
