# Commands

All commands run from repo root unless noted.

---

## Local dev (venv)

**Activate venv** (once per shell session):
```powershell
.venv\Scripts\Activate.ps1
```

**Run dev server** (hot reload):
```powershell
cd backend
..\.venv\Scripts\uvicorn.exe app.main:app --reload
```
API: http://localhost:8000  
Docs: http://localhost:8000/docs

**Run tests:**
```powershell
cd backend
python -m pytest -v
```

**Run single test file:**
```powershell
cd backend
python -m pytest tests/api/test_sessions.py -v
```

---

## Migrations (aerich)

Run from `backend/`:

**First time — init DB (creates tables from scratch):**
```powershell
cd backend
..\.venv\Scripts\aerich.exe init-db
```

**Generate migration after model change:**
```powershell
cd backend
..\.venv\Scripts\aerich.exe migrate --name "opisz_zmiane"
```

**Apply pending migrations:**
```powershell
cd backend
..\.venv\Scripts\aerich.exe upgrade
```

**Show migration history:**
```powershell
cd backend
..\.venv\Scripts\aerich.exe history
```

---

## Docker (standalone — SQLite)

**Build image:**
```powershell
docker build -t boardgames-backend ./backend
```

**Run container:**
```powershell
docker run -d --name boardgames -p 8000:8000 boardgames-backend
```

**Logs:**
```powershell
docker logs boardgames
docker logs -f boardgames   # follow
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

**Stop / remove:**
```powershell
docker rm -f boardgames
```

---

## Docker Compose (local dev z PostgreSQL)

**Start (build + run):**
```powershell
docker compose up --build
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

**Start w tle:**
```powershell
docker compose up --build -d
```

**Logi backendu:**
```powershell
docker compose logs -f backend
```

**Stop:**
```powershell
docker compose down
```

**Stop + usuń dane (volumes):**
```powershell
docker compose down -v
```

**Restart tylko backendu (po zmianie kodu):**
```powershell
docker compose up --build backend
```

---

## Instalacja zależności

**Dodaj pakiet:**
```powershell
.venv\Scripts\pip.exe install <package>
.venv\Scripts\pip.exe freeze > backend/requirements.txt
```

**Zainstaluj z requirements.txt:**
```powershell
.venv\Scripts\pip.exe install -r backend/requirements.txt
```
