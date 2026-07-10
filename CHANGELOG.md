# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-07-10

### Added
- **Monorepo Foundation**: Standardized monorepo directory layout containing backend, frontend, docs, scripts, infra, and github folders.
- **FastAPI Backend (Python 3.12)**:
  - Fast, modular ASGI backend initialized with `uv`.
  - Pydantic Settings integration for loading env variables from `.env` dynamically.
  - SQLAlchemy async PostgreSQL configuration with connection pooling (`asyncpg`).
  - Alembic migrations directory with custom async configuration and initial table revision.
  - Redis connection pool manager with dynamic health diagnostic checks.
  - JWT authentication flow featuring password hashing (`bcrypt`), access tokens, and a protected `/users/me` route.
  - Custom system middlewares: Request ID tracking, Loguru structured logs, Security headers, Rate limiter stubs, and Global Error handlers.
- **Next.js 15 Frontend (TypeScript & Tailwind CSS v4)**:
  - Premium dark-themed, glassmorphism UI layout featuring slate backgrounds and cyan accents.
  - Reusable layout views: Navbar and Footer components.
  - Standard App Router pages: Landing, Login, Registration, and protected Dashboard viewports.
  - Robust `apiClient` fetch wrapper supporting authorization headers, JSON payloads, and cookie forwarding credentials.
  - `useAuth` hook and Context Provider managing sessions and client routing redirects.
- **Docker Compose Environment**: Multi-container compose configuration running postgres, redis, and hot-reloaded backend/frontend code mounts.
- **CI / CD Workflow**: GitHub Actions script executing formatting audits, type verifications, build checks, and backend pytest suites.
- **Diagnostics**: Multi-route health controller checks (`/health`, `/health/db`, `/health/redis`).
- **Tests**: Pytest suite using in-memory SQLite transactions and mock health checkers, checking all user endpoints.
