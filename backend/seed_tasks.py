"""
InternX — Realistic Task Seeder
Run this script to populate the database with real internship simulation tasks.

Usage:
    cd backend
    python seed_tasks.py

Make sure your .env is loaded (uvicorn doesn't need to be running).
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

from app.core.database import db

# ── CONFIG ──────────────────────────────────────────────────────────────────
SPRINT_DURATION_DAYS = 14
START_DATE = datetime.now(timezone.utc)
END_DATE   = START_DATE + timedelta(days=SPRINT_DURATION_DAYS)

# Replace with your actual user ID from Supabase profiles table
# You can find it in Supabase → Table Editor → profiles
MENTOR_ID = "8a5160e7-9c80-4de3-9661-ddf7b60e1d79"  # your ID
INTERN_ID = "8a5160e7-9c80-4de3-9661-ddf7b60e1d79"  # same for now # ← CHANGE THIS (your ID: 8a5160e7-9c80-4de3-9661-ddf7b60e1d79)

def due(days_from_now):
    return (START_DATE + timedelta(days=days_from_now)).date().isoformat()

# ── TASKS BY ROLE ────────────────────────────────────────────────────────────
TASKS = {
    "frontend": [
        {
            "title": "Set up the project scaffold",
            "description": (
                "Initialize a new React + Vite project. Set up folder structure: "
                "src/components, src/pages, src/hooks, src/utils. Install Tailwind CSS, "
                "React Router, and Axios. Create a basic App.jsx with a placeholder route. "
                "Commit with message: 'chore: project scaffold'."
            ),
            "priority": "high",
            "due_days": 2,
            "resources": "https://vitejs.dev/guide/\nhttps://tailwindcss.com/docs/guides/vite\nhttps://reactrouter.com/en/main/start/tutorial",
        },
        {
            "title": "Build a reusable Button component",
            "description": (
                "Create a Button component that supports: variant (primary, secondary, ghost, danger), "
                "size (sm, md, lg), loading state with spinner, disabled state, and onClick handler. "
                "Write PropTypes or JSDoc for all props. Test it on a demo page."
            ),
            "priority": "medium",
            "due_days": 3,
            "resources": "https://www.figma.com/community/file/component-design-systems\nhttps://react.dev/reference/react/Component",
        },
        {
            "title": "Implement a responsive Navbar",
            "description": (
                "Build a Navbar component with: logo on the left, nav links in the center, "
                "user avatar + logout on the right. Must be fully responsive — hamburger menu on mobile. "
                "Use CSS transitions for mobile menu open/close. No external component libraries."
            ),
            "priority": "high",
            "due_days": 4,
            "resources": "https://tailwindcss.com/docs/responsive-design\nhttps://headlessui.com/",
        },
        {
            "title": "Build a Login form with validation",
            "description": (
                "Create a Login page with email and password fields. "
                "Validate: email must be valid format, password min 8 chars. "
                "Show inline error messages. On submit, call POST /api/auth/login "
                "and handle 401 (wrong credentials) and 500 (server error) gracefully. "
                "Show a loading spinner on the button while the request is in flight."
            ),
            "priority": "high",
            "due_days": 5,
            "resources": "https://react-hook-form.com/get-started\nhttps://zod.dev/",
        },
        {
            "title": "Create a Dashboard with charts",
            "description": (
                "Build a dashboard page that displays: total users (stat card), "
                "revenue this month (stat card), a line chart of daily signups for the last 30 days, "
                "and a pie chart of user roles. Use Recharts. Data can be hardcoded for now — "
                "focus on the UI, not the API integration."
            ),
            "priority": "medium",
            "due_days": 7,
            "resources": "https://recharts.org/en-US/guide\nhttps://www.figma.com/community/file/dashboard-design",
        },
        {
            "title": "Implement infinite scroll on a list page",
            "description": (
                "Create a /products page that fetches 20 items at a time from a mock API. "
                "Implement infinite scroll using IntersectionObserver (no library). "
                "Show a loading skeleton while fetching. Handle empty state and error state. "
                "Each product card should show: image, name, price, rating."
            ),
            "priority": "medium",
            "due_days": 9,
            "resources": "https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API\nhttps://dummyjson.com/docs/products",
        },
        {
            "title": "Add dark mode support",
            "description": (
                "Implement a dark/light mode toggle for the entire app. "
                "Use CSS variables for theming (not Tailwind dark: prefix). "
                "Persist the user's preference in localStorage. "
                "The toggle should be in the Navbar. All existing pages must look good in both modes."
            ),
            "priority": "low",
            "due_days": 11,
            "resources": "https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties",
        },
        {
            "title": "Write unit tests for your components",
            "description": (
                "Set up Vitest + React Testing Library. Write tests for: "
                "Button (renders correctly, shows spinner when loading, disabled when disabled), "
                "Login form (shows errors on invalid input, submits with valid data), "
                "Navbar (renders links, mobile menu opens on hamburger click). "
                "Aim for >80% coverage on these components."
            ),
            "priority": "high",
            "due_days": 13,
            "resources": "https://vitest.dev/guide/\nhttps://testing-library.com/docs/react-testing-library/intro/",
        },
    ],

    "backend": [
        {
            "title": "Set up FastAPI project structure",
            "description": (
                "Initialize a FastAPI project with: app/routers/, app/models/, app/schemas/, "
                "app/core/ (config, database, auth). Set up .env with pydantic Settings. "
                "Connect to a PostgreSQL database using asyncpg. Add a /health endpoint that returns status and db ping."
            ),
            "priority": "high",
            "due_days": 2,
            "resources": "https://fastapi.tiangolo.com/tutorial/bigger-applications/\nhttps://docs.pydantic.dev/latest/concepts/pydantic_settings/",
        },
        {
            "title": "Design and create the database schema",
            "description": (
                "Design an ERD for a simple e-commerce system: users, products, orders, order_items, reviews. "
                "Write the SQL CREATE TABLE statements with proper foreign keys, indexes, and constraints. "
                "Add created_at/updated_at to every table. Run migrations using Alembic."
            ),
            "priority": "high",
            "due_days": 3,
            "resources": "https://alembic.sqlalchemy.org/en/latest/tutorial.html\nhttps://dbdiagram.io/",
        },
        {
            "title": "Build CRUD API for Products",
            "description": (
                "Create REST endpoints: GET /products (paginated, filterable by category and price range), "
                "GET /products/{id}, POST /products (admin only), PUT /products/{id} (admin only), "
                "DELETE /products/{id} (admin only). Use Pydantic schemas for request/response validation. "
                "Return proper HTTP status codes."
            ),
            "priority": "high",
            "due_days": 5,
            "resources": "https://fastapi.tiangolo.com/tutorial/response-model/\nhttps://fastapi.tiangolo.com/tutorial/query-params/",
        },
        {
            "title": "Implement JWT authentication",
            "description": (
                "Build POST /auth/register and POST /auth/login endpoints. "
                "Hash passwords with bcrypt. Return a JWT access token (15min expiry) "
                "and refresh token (7 days). Implement a /auth/refresh endpoint. "
                "Create a get_current_user dependency that decodes the JWT and returns the user."
            ),
            "priority": "high",
            "due_days": 6,
            "resources": "https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/\nhttps://python-jose.readthedocs.io/",
        },
        {
            "title": "Add rate limiting and request validation",
            "description": (
                "Install slowapi and add rate limiting: 100 requests/min per IP globally, "
                "5 requests/min on POST /auth/login. Add request size limiting (max 10MB). "
                "Add input sanitization to prevent SQL injection on any raw query. "
                "Write a custom exception handler that returns consistent error response format."
            ),
            "priority": "medium",
            "due_days": 8,
            "resources": "https://slowapi.readthedocs.io/en/latest/\nhttps://fastapi.tiangolo.com/tutorial/handling-errors/",
        },
        {
            "title": "Build a background task system",
            "description": (
                "Use Celery + Redis to create background tasks: "
                "send_welcome_email (triggered on registration), "
                "process_order (triggered on order creation — reduces stock, sends confirmation). "
                "Add a task status endpoint: GET /tasks/{task_id}. "
                "Use flower to monitor tasks locally."
            ),
            "priority": "medium",
            "due_days": 10,
            "resources": "https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html\nhttps://flower.readthedocs.io/",
        },
        {
            "title": "Write API tests with pytest",
            "description": (
                "Set up pytest with a test database (SQLite for speed). "
                "Write tests for: auth (register, login, invalid credentials, token refresh), "
                "products (CRUD, pagination, filtering, unauthorized access). "
                "Use httpx.AsyncClient for async tests. Aim for >85% coverage. "
                "Add a GitHub Actions workflow that runs tests on every push."
            ),
            "priority": "high",
            "due_days": 13,
            "resources": "https://fastapi.tiangolo.com/tutorial/testing/\nhttps://pytest.org/",
        },
    ],

    "fullstack": [
        {
            "title": "Plan the full stack architecture",
            "description": (
                "Write a 1-page architecture document for a real-time chat app. Include: "
                "tech stack choices with justification (frontend framework, backend, database, websocket), "
                "system diagram showing all components, API contract (list of endpoints with request/response shapes), "
                "database schema, deployment plan. Use draw.io or Excalidraw for diagrams."
            ),
            "priority": "high",
            "due_days": 2,
            "resources": "https://excalidraw.com/\nhttps://www.notion.so/templates/technical-design-doc",
        },
        {
            "title": "Build the backend API and database",
            "description": (
                "Implement: user registration/login with JWT, "
                "chat rooms (create, list, join), messages (send, paginated history). "
                "Use FastAPI + PostgreSQL. Messages must be stored with: id, room_id, user_id, content, created_at. "
                "Add WebSocket endpoint: ws://localhost:8000/ws/{room_id} that broadcasts messages to all connected clients."
            ),
            "priority": "high",
            "due_days": 6,
            "resources": "https://fastapi.tiangolo.com/advanced/websockets/\nhttps://www.postgresql.org/docs/",
        },
        {
            "title": "Build the React frontend",
            "description": (
                "Create: Login page, Room list page, Chat room page. "
                "The chat room must connect to the WebSocket and show messages in real-time. "
                "New messages appear at the bottom. Auto-scroll to latest message. "
                "Show online users count. Handle disconnect/reconnect gracefully."
            ),
            "priority": "high",
            "due_days": 9,
            "resources": "https://developer.mozilla.org/en-US/docs/Web/API/WebSocket\nhttps://react.dev/",
        },
        {
            "title": "Add CI/CD pipeline",
            "description": (
                "Set up GitHub Actions with two workflows: "
                "1) test.yml — runs backend pytest and frontend Vitest on every PR. "
                "2) deploy.yml — on merge to main, builds Docker image, pushes to Docker Hub, "
                "deploys to a free Render instance. Write a docker-compose.yml for local development "
                "that spins up frontend, backend, postgres, and redis together."
            ),
            "priority": "medium",
            "due_days": 12,
            "resources": "https://docs.github.com/en/actions\nhttps://docs.docker.com/compose/",
        },
    ],

    "devops": [
        {
            "title": "Containerize a Node.js app with Docker",
            "description": (
                "Take the provided Node.js Express app and write a Dockerfile: "
                "use node:20-alpine as base, copy only necessary files, run as non-root user, "
                "expose port 3000, use multi-stage build to keep image small. "
                "Build the image and verify it runs. Image must be under 150MB."
            ),
            "priority": "high",
            "due_days": 2,
            "resources": "https://docs.docker.com/language/nodejs/containerize/\nhttps://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/",
        },
        {
            "title": "Write a docker-compose for a full stack app",
            "description": (
                "Write docker-compose.yml that brings up: "
                "frontend (React, port 3000), backend (FastAPI, port 8000), "
                "postgres (port 5432, with volume for persistence), redis (port 6379). "
                "Backend must wait for postgres to be healthy before starting. "
                "Add environment variable support via .env file. Include a README with setup instructions."
            ),
            "priority": "high",
            "due_days": 4,
            "resources": "https://docs.docker.com/compose/compose-file/\nhttps://docs.docker.com/compose/startup-order/",
        },
        {
            "title": "Set up a CI pipeline with GitHub Actions",
            "description": (
                "Create .github/workflows/ci.yml that: "
                "triggers on push to main and on PRs, "
                "runs in parallel: backend tests (pytest), frontend tests (vitest), linting (ruff + eslint). "
                "Fails the pipeline if any step fails. "
                "Add a badge to the README showing build status."
            ),
            "priority": "high",
            "due_days": 6,
            "resources": "https://docs.github.com/en/actions/writing-workflows\nhttps://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python",
        },
        {
            "title": "Deploy to the cloud with Infrastructure as Code",
            "description": (
                "Use Terraform to provision on AWS free tier: "
                "1 EC2 t2.micro instance, 1 RDS PostgreSQL db.t3.micro, "
                "1 S3 bucket for static assets, security groups with least-privilege access. "
                "Write a deploy script that SSHs into EC2 and runs docker-compose up. "
                "Document every resource created and its cost."
            ),
            "priority": "medium",
            "due_days": 10,
            "resources": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs\nhttps://aws.amazon.com/free/",
        },
        {
            "title": "Set up monitoring and alerting",
            "description": (
                "Install Prometheus + Grafana using docker-compose. "
                "Instrument the FastAPI app to expose /metrics endpoint. "
                "Create a Grafana dashboard showing: request rate, error rate, p95 latency, CPU/memory. "
                "Set up an alert that fires when error rate > 5% for 2 minutes. "
                "Document how to access the dashboards."
            ),
            "priority": "medium",
            "due_days": 13,
            "resources": "https://prometheus.io/docs/introduction/overview/\nhttps://grafana.com/docs/grafana/latest/getting-started/",
        },
    ],

    "design": [
        {
            "title": "Conduct user research and create personas",
            "description": (
                "Interview 3 people (can be friends/family) about their experience using a food delivery app. "
                "Create 2 user personas based on your findings — each with: name, age, occupation, goals, frustrations, tech comfort level. "
                "Write a 1-page research summary. Present in a Figma file with a clean layout."
            ),
            "priority": "high",
            "due_days": 3,
            "resources": "https://www.figma.com/community/file/user-persona-template\nhttps://www.nngroup.com/articles/persona/",
        },
        {
            "title": "Create a design system in Figma",
            "description": (
                "Build a design system for a fintech app with: color palette (primary, secondary, semantic colors), "
                "typography scale (display, heading, body, caption — with sizes and weights), "
                "spacing system (4px base grid), component library: Button (5 variants), Input (4 states), "
                "Card, Badge, Avatar. All components must use Figma auto-layout and be properly named."
            ),
            "priority": "high",
            "due_days": 5,
            "resources": "https://www.figma.com/community/file/design-system-template\nhttps://m3.material.io/",
        },
        {
            "title": "Design onboarding flow wireframes",
            "description": (
                "Design low-fidelity wireframes for a 5-screen onboarding flow for a fitness app: "
                "welcome screen, goal selection, fitness level assessment, schedule setup, notification preferences. "
                "Show mobile (375px) and tablet (768px) layouts. "
                "Add annotations explaining UX decisions. Use your design system components."
            ),
            "priority": "medium",
            "due_days": 7,
            "resources": "https://www.nngroup.com/articles/mobile-ux/\nhttps://www.figma.com/community/file/wireframe-kit",
        },
        {
            "title": "Create high-fidelity UI screens",
            "description": (
                "Convert your wireframes into polished high-fidelity designs. "
                "Apply your design system. Use real content (not Lorem Ipsum). "
                "Add micro-interaction annotations (what happens on button tap, transitions between screens). "
                "Export assets at 1x, 2x, 3x. Write a handoff document for developers."
            ),
            "priority": "high",
            "due_days": 10,
            "resources": "https://www.figma.com/community/file/mobile-ui-kit\nhttps://zeroheight.com/",
        },
        {
            "title": "Run usability testing and iterate",
            "description": (
                "Run a usability test with 3 participants on your high-fidelity prototype. "
                "Give them 3 tasks: complete onboarding, set a fitness goal, change notification settings. "
                "Record time-on-task, errors, and satisfaction rating (1-5). "
                "Create an affinity diagram of findings. Make at least 5 design changes based on feedback."
            ),
            "priority": "medium",
            "due_days": 13,
            "resources": "https://www.nngroup.com/articles/usability-testing-101/\nhttps://maze.co/",
        },
    ],
}


def seed():
    print("🌱 InternX Task Seeder")
    print("=" * 50)

    # Get the intern's actual role from the database
    profile = db.table("profiles").select("*").eq("id", INTERN_ID).execute()
    if not profile.data:
        print(f"❌ No profile found for INTERN_ID: {INTERN_ID}")
        print("   Update INTERN_ID at the top of this file.")
        sys.exit(1)

    intern_role = profile.data[0].get("intern_role", "frontend")
    print(f"✓ Found intern: {profile.data[0].get('name')} (role: {intern_role})")

    # Create sprint
    print(f"\n📅 Creating sprint ({START_DATE.date()} → {END_DATE.date()})...")
    sprint_result = db.table("sprints").insert({
        "title": f"Sprint 1 — {intern_role.title()} Internship",
        "description": f"A realistic 2-week {intern_role} internship simulation with real-world tasks.",
        "start_date": START_DATE.date().isoformat(),
        "end_date": END_DATE.date().isoformat(),
        "is_active": True,
        "created_by": MENTOR_ID if MENTOR_ID != "00000000-0000-0000-0000-000000000000" else INTERN_ID,
    }).execute()

    sprint_id = sprint_result.data[0]["id"]
    print(f"✓ Sprint created: {sprint_id}")

    # Seed tasks for the intern's role
    tasks = TASKS.get(intern_role, TASKS["frontend"])
    print(f"\n📋 Seeding {len(tasks)} tasks for {intern_role} intern...")

    now = datetime.now(timezone.utc).isoformat()
    created = 0

    for task in tasks:
        try:
            db.table("tasks").insert({
                "title": task["title"],
                "description": task["description"],
                "sprint_id": sprint_id,
                "assigned_to": INTERN_ID,
                "intern_role": intern_role,
                "priority": task["priority"],
                "due_date": due(task["due_days"]),
                "resources": task.get("resources", ""),
                "status": "todo",
                "created_by": MENTOR_ID if MENTOR_ID != "00000000-0000-0000-0000-000000000000" else INTERN_ID,
                "created_at": now,
                "updated_at": now,
            }).execute()
            print(f"  ✓ {task['title']}")
            created += 1
        except Exception as e:
            print(f"  ✗ {task['title']}: {e}")

    print(f"\n🎉 Done! Created {created}/{len(tasks)} tasks.")
    print(f"\nGo to: http://localhost:3000/dashboard")
    print("You should see your full internship task board!")


if __name__ == "__main__":
    # Quick check
    if INTERN_ID == "00000000-0000-0000-0000-000000000000":
        print("⚠️  Please update INTERN_ID in this file before running.")
        print("   Your ID is: 8a5160e7-9c80-4de3-9661-ddf7b60e1d79")
        print("   MENTOR_ID can be the same as INTERN_ID for now.")
        sys.exit(1)
    seed()