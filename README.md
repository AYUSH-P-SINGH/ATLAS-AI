# Atlas AI — Software Architecture Copilot

Atlas AI is an AI-powered platform that understands an entire software repository, builds a semantic representation of its architecture, and helps developers understand, review, improve, and document large codebases.

"GitHub Copilot helps write code. Atlas AI helps understand and improve software architecture."

---

## 🏗️ Project Architecture (Phase 1)

```text
atlas-ai/
├── frontend/             # Next.js 15 App (React 19, TypeScript, Tailwind CSS v4)
│   ├── app/              # App router views (Landing, Auth, Protected Dashboard)
│   ├── components/       # Reusable layout components (Navbar, Footer)
│   ├── hooks/            # Session React contexts (useAuth hook)
│   └── services/         # Custom fetch client wrapper (apiClient)
├── backend/              # FastAPI Application (Python 3.12, Uvicorn, SQLAlchemy v2)
│   ├── app/
│   │   ├── api/          # Route controller routers (Auth, Users, Health)
│   │   ├── core/         # Core initializers (Config settings, DB pooling, Redis client)
│   │   ├── middleware/   # Request-response filters (CORS, Request ID, Logging, Security)
│   │   ├── models/       # Database entities (SQLAlchemy User model)
│   │   ├── schemas/      # Input validation & serialization schemas (Pydantic)
│   │   ├── services/     # Business logic layers (Auth Service logic)
│   │   └── repositories/ # Database query abstraction (User Repository)
│   └── migrations/       # Alembic async migration files
├── docker-compose.yml    # Development environment compose template
└── README.md             # This document
```

---

## 🛠️ API Documentation (Endpoints)

All API endpoints are prefixed with `/api`.

### Authentication
* **POST `/api/auth/register`**: Register a new user profile.
  * *Request Body*: `{"email": "...", "username": "...", "password": "..."}`
  * *Response*: User profile metadata.
* **POST `/api/auth/login`**: Authenticate credentials, write an `HttpOnly` JWT cookie, and return token details.
  * *Request Body*: `{"username_or_email": "...", "password": "..."}`
  * *Response*: `{"access_token": "...", "token_type": "bearer"}`
* **POST `/api/auth/logout`**: Clear JWT authorization cookies.
  * *Response*: Successful logout confirmation.

### User Profiles
* **GET `/api/users/me`**: Fetch authenticated user profile details. *Requires JWT cookie or authorization header.*
  * *Response*: User profile model matching the current token session.

### System Diagnostics
* **GET `/api/health`**: Basic API status check.
* **GET `/api/health/db`**: Database connectivity latency check.
* **GET `/api/health/redis`**: Redis cache connectivity latency check.

---

## 🚀 Getting Started (Local Development)

### Docker Compose (Recommended)
Launch the entire system including databases and caches with one command:
```bash
docker compose up --build
```
* Frontend client: [http://localhost:3000](http://localhost:3000)
* Backend API: [http://localhost:8000](http://localhost:8000)
* API Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Direct Host Setup
Ensure **PostgreSQL 15+** and **Redis** are installed and running locally.

1. **Database Setup**:
   * Set up a database named `atlas_db`.
   * Configure environment variables in `backend/.env` (use `backend/.env.example` as a template).

2. **Run Backend Services**:
   ```bash
   cd backend
   # Install dependencies and start FastAPI using uv:
   uv run uvicorn app.main:app --reload --port 8000
   ```

3. **Run Frontend Client**:
   ```bash
   cd frontend
   # Install node dependencies and start dev server:
   npm install
   npm run dev
   ```

---

## 🎯 Project Development Roadmap

1. **Phase 1: Foundation & Project Initialization** (Current)
   * Setup monorepo, FastAPI backend, Next.js 15 client, PostgreSQL, Redis, JWT auth, logging, middlewares, and CI.
2. **Phase 2: Repository Ingestion & Indexing**
   * Clone public/private Git repositories, unzip uploads, auto-detect file formats, parse trees, and queue ingestion.
3. **Phase 3: AST Parsing & Dependency Graphs**
   * Parse abstract syntax trees across typescript/python/etc. to build node import-export mapping graphs.
4. **Phase 4: Multi-Database Integration**
   * Connect PostgreSQL (entities), Neo4j (relationship maps), and pgvector (semantic search vectors).
5. **Phase 5: Embedding Pipeline & Hybrid Search**
   * Slice files into logical blocks, generate embeddings, and configure BM25 + Vector hybrid searches.
6. **Phase 6: Codebase Chat with GraphRAG**
   * Integrate LLMs using graph-guided search retrieval to answer architectural queries with exact citations.
7. **Phase 7: Diagram Generator**
   * Render dynamic system, service, class, and database maps using Mermaid.js and React Flow.
8. **Phase 8: Multi-Agent Workflows**
   * Build specialised agents (Security, Performance, Architect, documentation) orchestrated using LangGraph.
9. **Phase 9: Code Smells & SOLID Checks**
   * Detect anti-patterns, God classes, circular references, and code violations.
10. **Phase 10: PR Review & Impact Analyst**
    * Automatically parse commits to predict blast radius of changes and suggest design refactors.
11. **Phase 11: Production Deployment & Monitoring**
    * Build Docker images, compile Kubernetes specs, and wire up Prometheus + Grafana dashboards.
12. **Phase 12: Evaluation & Production Release**
    * Performance benchmarking, memory profiling, and final release preparation.
