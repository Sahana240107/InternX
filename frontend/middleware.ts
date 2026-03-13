import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// This runs before EVERY page load in the /dashboard/* routes
// It checks if the user has a token in localStorage (via cookie fallback)
// If not, it redirects them to the login page

// Routes that don't need a login
const PUBLIC_ROUTES = ['/auth/login', '/auth/callback', '/auth/onboarding', '/']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Let public routes through
  if (PUBLIC_ROUTES.some(route => pathname.startsWith(route))) {
    return NextResponse.next()
  }

  // For protected routes, check for the auth token in cookies
  // (We store it in a cookie in addition to localStorage for SSR)
  const token = request.cookies.get('internx-token')?.value

  if (!token && pathname.startsWith('/dashboard')) {
    const loginUrl = new URL('/auth/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  // Only run middleware on these paths (not on _next/static, images, etc.)
  matcher: ['/dashboard/:path*', '/internship/:path*', '/profile/:path*'],
}
