import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center" style={{ background: 'var(--surface)' }}>
      <div className="text-center animate-fade-up">
        <div className="w-16 h-16 rounded-2xl flex items-center justify-center font-display font-bold text-white text-2xl mx-auto mb-6"
          style={{ background: 'var(--accent)' }}>X</div>
        <h1 className="text-5xl font-display mb-3" style={{ color: 'var(--ink)' }}>InternX</h1>
        <p className="text-lg mb-8" style={{ color: 'var(--ink-muted)' }}>AI-Powered Virtual Internship Simulator</p>
        <Link href="/auth/login" className="btn-primary px-8 py-4 text-base">
          Get Started →
        </Link>
      </div>
    </main>
  )
}
