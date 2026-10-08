# CosmicLens

Explainable AI for Discovering and Understanding Change in the Infrared Sky.

CosmicLens is an explainable AI-powered discovery platform designed for SPHEREx-style infrared survey analysis. The project is built around a single fast-track hackathon development model: one developer, one integrated pipeline, and a complete end-to-end discovery story that works in under 24 hours.

## Phase 0: foundation and project scaffolding

This repository now includes the initial starter structure for:
- a Next.js + TypeScript frontend
- a FastAPI backend
- a shared development workflow
- a local Docker-based setup for rapid iteration

## Stack
- Frontend: Next.js 14 + TypeScript + Tailwind CSS
- Backend: FastAPI + Python 3.11
- Data/ML: NumPy, pandas, SciPy, scikit-learn
- Infra: Docker + docker-compose

## Local development

### 1) Start backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Start frontend

```bash
cd frontend
npm install
npm run dev
```

### 3) Or run both with Docker

```bash
docker compose up --build
```

## Project layout

```text
.
├── backend/                 Python API and analysis pipeline
├── frontend/                Next.js app
├── .env.example             Sample environment variables
├── .gitignore
├── docker-compose.yml       Local orchestration for frontend + backend
├── LICENSE
└── README.md
```

## Goal for this phase

Phase 0 is intentionally light: set up the repo, establish the separation of concerns, and make the next steps easy. The next phase will focus on the real demo story: sky explorer, time machine, anomaly scoring, and explainability.
