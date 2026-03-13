'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store/authStore'
import api from '@/lib/api'
import { toast } from 'sonner'

const ROLES = [
  { id: 'frontend',  label: 'Frontend Developer',  desc: 'HTML, CSS, React, UI/UX',            icon: '🎨' },
  { id: 'backend',   label: 'Backend Developer',    desc: 'APIs, databases, server logic',       icon: '⚙️' },
  { id: 'fullstack', label: 'Full Stack Developer', desc: 'Both frontend and backend',           icon: '🔥' },
  { id: 'devops',    label: 'DevOps Engineer',      desc: 'CI/CD, cloud, infrastructure',        icon: '🚀' },
  { id: 'design',    label: 'UI/UX Designer',       desc: 'Figma, user research, prototyping',   icon: '✏️' },
]

export default function OnboardingPage() {
  const router      = useRouter()
  const { user, setAuth, token } = useAuthStore()
  const [selected,  setSelected]  = useState<string | null>(null)
  const [saving,    setSaving]    = useState(false)

  const handleSave = async () => {
    if (!selected) return
    setSaving(true)
    try {
      const { data } = await api.put('/api/auth/me', { intern_role: selected })
      // Update the user in the global store with the new intern_role
      setAuth(data, token!)
      toast.success('Welcome to InternX! Your internship begins now.')
      router.replace('/dashboard')
    } catch {
      toast.error('Something went wrong. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 to-white flex items-center justify-center px-4">
      <div className="w-full max-w-2xl">

        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome, {user?.name?.split(' ')[0]}! 👋
          </h1>
          <p className="mt-2 text-gray-500">
            Choose your internship role. You&apos;ll receive tasks specific to this role.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
          {ROLES.map((role) => (
            <button
              key={role.id}
              onClick={() => setSelected(role.id)}
              className={`
                text-left p-5 rounded-xl border-2 transition-all duration-150
                ${selected === role.id
                  ? 'border-indigo-500 bg-indigo-50 shadow-md'
                  : 'border-gray-200 bg-white hover:border-indigo-300 hover:shadow-sm'
                }
              `}
            >
              <span className="text-3xl">{role.icon}</span>
              <p className="mt-2 font-semibold text-gray-900">{role.label}</p>
              <p className="text-sm text-gray-500 mt-1">{role.desc}</p>
            </button>
          ))}
        </div>

        <button
          onClick={handleSave}
          disabled={!selected || saving}
          className="w-full py-3 px-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold rounded-xl transition-colors"
        >
          {saving ? 'Saving...' : 'Start My Internship →'}
        </button>
      </div>
    </main>
  )
}
