# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

BoardGamesCounter — app for tracking board game scores/results. FastAPI backend (REST API), planned frontend TBD.

## Running

Backend dev server (from `backend/`):
```powershell
.venv\Scripts\uvicorn.exe app.main:app --reload
```

Legacy entry point (unused, PyCharm default):
```powershell
.venv\Scripts\python.exe main.py
```

## Environment

- Python virtual environment at `.venv/` (Python 3.14)
- Activate with `.venv\Scripts\Activate.ps1` before installing packages
- Install dependencies: `.venv\Scripts\pip.exe install <package>`
- Backend dependencies: `backend/requirements.txt`

## Architecture

```
BoardGamesCounter/
├── backend/                  FastAPI REST API
│   ├── app/
│   │   ├── main.py           FastAPI app entry point, lifespan, router registration
│   │   ├── config.py         Settings via pydantic-settings (.env), DATABASE_URL, TORTOISE_ORM config
│   │   ├── models/           Tortoise ORM database models
│   │   │   ├── game.py       Game (name, min/max players)
│   │   │   ├── player.py     Player (name)
│   │   │   └── session.py    GameSession (game FK, played_at, notes) + Score (session FK, player FK, points, winner)
│   │   ├── schemas/          Pydantic request/response schemas (validation layer)
│   │   │   ├── game.py
│   │   │   ├── player.py
│   │   │   └── session.py
│   │   ├── services/         Business logic layer (DB queries, data manipulation)
│   │   │   ├── game.py
│   │   │   ├── player.py
│   │   │   └── session.py
│   │   └── api/v1/routes/    HTTP route handlers (thin — delegate to services)
│   │       ├── games.py
│   │       ├── players.py
│   │       └── sessions.py
│   ├── tests/                pytest test suite
│   ├── migrations/           aerich DB migrations (to be created)
│   ├── requirements.txt      Python dependencies
│   ├── pyproject.toml        aerich config
│   └── .env.example          Example env vars
├── main.py                   Unused PyCharm stub — ignore
└── .venv/                    Python 3.14 virtual environment
```

## Database

- ORM: Tortoise ORM (async)
- Migrations: aerich
- Dev: SQLite (`sqlite://./db.sqlite3`)
- Prod: PostgreSQL (set `DATABASE_URL` env var)

Init migrations (first time):
```powershell
cd backend
..\.venv\Scripts\aerich.exe init-db
```

Run migrations:
```powershell
..\.venv\Scripts\aerich.exe upgrade
```

## Deployment Plan

Target: free hosting via **Render** (render.com).

### Why Render
- Free tier supports Docker containers
- Free PostgreSQL (90 days, then cheap)
- Native GitHub Actions integration — push to `main` triggers deploy
- No credit card required for free tier

### Docker plan
- `backend/Dockerfile` — multi-stage build (build deps → slim runtime)
- `docker-compose.yml` — local dev with PostgreSQL container
- `.dockerignore` — exclude `.venv/`, `__pycache__/`, `.env`

### GitHub Actions plan
- `.github/workflows/ci.yml` — run tests on every PR
- `.github/workflows/deploy.yml` — deploy to Render on push to `main`
- Render deploy hook URL stored as GitHub secret `RENDER_DEPLOY_HOOK`

### Status
- [x] Dockerfile (`backend/Dockerfile`, multi-stage, python:3.13-slim)
- [x] docker-compose.yml (local dev with PostgreSQL 16)
- [ ] GitHub Actions CI (tests)
- [ ] GitHub Actions CD (Render deploy)
- [ ] Render service setup
- [ ] PostgreSQL migration in prod
