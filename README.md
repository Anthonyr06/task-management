# Prueba Técnica — Senior Fullstack (Backend-focused)

Implementación de un **API de Gestión de Tareas Colaborativas** (FastAPI + SQLAlchemy + PostgreSQL + Redis) y un **frontend simple** (React + Vite) que consume el API. Incluye además una sección de **Diseño de Sistema** para un e-commerce (Parte 1 del documento). 

## Stack
- Backend: Python 3.11+, FastAPI, SQLAlchemy, Alembic
- DB: PostgreSQL
- Cache/Infra: Redis
- Frontend: React 18 + Vite + TypeScript
- Containerización: Docker + docker-compose 

---

## Quickstart (Docker Compose)

### 1) Variables de entorno
Crea archivos `.env` según corresponda (ejemplos abajo). También puedes usar `.env.example` como referencia.

### 2) Levantar todo
Desde la raíz del repo:

```bash
docker compose up --build
