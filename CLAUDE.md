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
│   ├── migrations/           aerich DB migrations
│   ├── requirements.txt      Python dependencies (prod)
│   ├── requirements-dev.txt  Python dependencies (dev + test)
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

Target: **Render** (web service, free tier) + **Neon.tech** (PostgreSQL, free tier).

### Why Render + Neon
- Render free: Docker containers, no credit card, cold start ~1min after inactivity (acceptable — app used ~once/2 weeks)
- Neon free: PostgreSQL 0.5GB, **no expiry, no pause** — unlike Render PG (30-day expiry) or Supabase (pauses after 1 week)
- Both free, no credit card required

### Docker
- `backend/Dockerfile` — multi-stage build (build deps → slim runtime)
- `docker-compose.yml` — local dev with PostgreSQL 16 container
- `.dockerignore` — exclude `.venv/`, `__pycache__/`, `.env`
- `backend/entrypoint.sh` — runs `aerich upgrade` then starts uvicorn

### GitHub Actions
- `.github/workflows/ci.yml` — run tests on every push/PR to master
- `.github/workflows/deploy.yml` — deploy to Render on push to `master` (TODO)
- Render deploy hook URL stored as GitHub secret `RENDER_DEPLOY_HOOK`

### Status
- [x] Dockerfile (`backend/Dockerfile`, multi-stage, python:3.13-slim)
- [x] docker-compose.yml (local dev with PostgreSQL 16)
- [x] GitHub Actions CI (tests via pytest)
- [ ] GitHub Actions CD (Render deploy hook)
- [ ] Render service setup
- [ ] Neon PostgreSQL setup + DATABASE_URL secret
