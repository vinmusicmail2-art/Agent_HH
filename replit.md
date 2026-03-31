# Agent HH — Job Search App

A web application for searching job vacancies on HH.ru (HeadHunter).

## Architecture

- **Backend**: FastAPI (Python) — serves both the REST API and the frontend HTML
- **Frontend**: Vanilla HTML/CSS/JS served by FastAPI as a static file

## Structure

```
agent-hh/
├── backend/
│   ├── main.py            # FastAPI server — API routes + serves frontend/index.html
│   └── requirements.txt   # Python dependencies (fastapi, uvicorn, httpx, gunicorn)
├── frontend/
│   └── index.html         # Full UI (HTML + CSS + JS)
└── replit.md
```

## Running (Development)

The app runs as a single process on port 5000:

```
uvicorn backend.main:app --host 0.0.0.0 --port 5000
```

## Key Details

- API base: `/api` (relative URLs, no hardcoded host)
- Backend proxies HH.ru API calls via `httpx`
- Frontend uses `localStorage` for starred/favorite vacancies
- Vacancy preview uses `<iframe>` (adapted from Electron's `<webview>`)
- CORS is open (`allow_origins=["*"]`) for development

## Deployment

- Target: autoscale
- Run: `gunicorn --bind=0.0.0.0:5000 --reuse-port -k uvicorn.workers.UvicornWorker backend.main:app`
