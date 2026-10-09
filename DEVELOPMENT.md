# SKYTRACE AI — Local Development & Build Guide

## Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Git

---

## 1. Backend Setup

```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend:
- Health check: `http://localhost:8000/api/health`
- OpenAPI Swagger docs: `http://localhost:8000/docs`

---

## 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 3. Running Scientific Tests

```bash
cd backend
pytest tests/
```

---

## 4. Docker Compose Setup

```bash
docker compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
