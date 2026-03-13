export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-brand-50 to-indigo-100">
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold text-brand-900">InternX</h1>
        <p className="text-xl text-gray-600">AI-Powered Virtual Internship Simulator</p>
        <a
          href="/auth/login"
          className="inline-block mt-4 px-8 py-3 bg-brand-600 text-white rounded-lg font-medium hover:bg-brand-700 transition-colors"
        >
          Get Started
        </a>
      </div>
    </main>
  )
}
