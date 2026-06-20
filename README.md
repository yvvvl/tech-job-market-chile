# Tech Job Market Intelligence Chile

[![CI](https://github.com/yvvvl/tech-job-market-chile/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/yvvvl/tech-job-market-chile/actions/workflows/ci.yml)

**Demo:** https://tech-job-market-chile-demo.silva-ignacio-696.workers.dev/  
**API local:** http://localhost:8000/docs

Plataforma full-stack para transformar ofertas laborales TI en información útil sobre tecnologías, seniority, categorías, ubicación, salarios y rutas de aprendizaje.

> **Transparencia de datos:** la demo pública utiliza un dataset simulado y versionado para mantenerse disponible sin costo. El backend real permite validar e importar CSV curados. El proyecto no realiza scraping automático ni presenta los datos simulados como estadísticas oficiales.

## Qué demuestra este proyecto

- Diseño de una API REST con FastAPI y contratos OpenAPI.
- Modelado relacional con PostgreSQL, SQLAlchemy y relaciones muchos-a-muchos.
- Migraciones de base de datos con Alembic.
- Pipeline de validación, clasificación e importación de CSV.
- Métricas de calidad de datos, filtros y recomendaciones basadas en reglas.
- Dashboard en React y TypeScript con visualizaciones interactivas.
- Pruebas unitarias y de integración con Pytest.
- CI con GitHub Actions para backend y frontend.
- Entorno reproducible con Docker Compose.
- Despliegue de demo estática en Cloudflare.

## Vista del producto

### Dashboard

![Dashboard general](docs/images/dashboard-overview.png)

![Analítica del dashboard](docs/images/dashboard-analytics.png)

### Technology Explorer

![Explorador de tecnologías](docs/images/technology-explorer.png)

### Career Recommendations

![Rutas de aprendizaje](docs/images/career-recommendations.png)

<details>
<summary>API y calidad de datos</summary>

![Documentación OpenAPI](docs/images/api-documentation.png)

![Endpoint overview](docs/images/bruno-overview.png)

![Endpoint de calidad de datos](docs/images/bruno-data-quality.png)

</details>

## Arquitectura

```text
CSV curado o dataset de ejemplo
           |
           v
Validación y normalización
           |
           v
PostgreSQL + SQLAlchemy + Alembic
           |
           v
FastAPI /api/v1
           |
           v
React + TypeScript + React Query
```

### Componentes principales

```text
backend/
  app/
    database/       Modelos, sesión y acceso a PostgreSQL
    pipeline/       Extracción de tecnologías y clasificación
    routers/        Endpoints de salud, estadísticas y recomendaciones
    schemas/        Contratos Pydantic/OpenAPI
    services/       Lógica de estadísticas y recomendaciones
    scripts/        Seed, validación e importación
  alembic/          Migraciones
  tests/            Pruebas unitarias y de integración
frontend/
  src/lib/api/      Cliente y contratos TypeScript
  src/routes/       Dashboard, Explorer y Recommendations
data/seeds/         Dataset de ejemplo versionado
.github/workflows/  Pipeline de CI
```

`data/raw/` se mantiene fuera de Git mediante `.gitignore`; allí puede colocarse un CSV real curado localmente.

## Stack

**Backend:** Python 3.12, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, Uvicorn.  
**Frontend:** React, TypeScript, Vite, TanStack Router, React Query, Tailwind CSS, shadcn/ui, Recharts.  
**Calidad e infraestructura:** Pytest, Ruff, ESLint, Docker Compose, GitHub Actions, Cloudflare Workers.

## Inicio rápido

### Requisitos

- Python 3.12+
- Node.js 20+
- Docker y Docker Compose

### 1. Clonar

```bash
git clone https://github.com/yvvvl/tech-job-market-chile.git
cd tech-job-market-chile
```

### 2. Levantar PostgreSQL

```bash
docker compose up -d
```

### 3. Backend

En Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements-dev.txt
```

Crear `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg2://techuser:techpass@localhost:5433/tech_jobs_chile
FRONTEND_URL=http://localhost:5173
```

Aplicar migraciones y cargar el dataset de ejemplo:

```powershell
cd backend
python -m alembic upgrade head
python -m app.scripts.seed_data
python -m uvicorn app.main:app --reload
```

API: http://localhost:8000  
OpenAPI: http://localhost:8000/docs

### 4. Frontend

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Endpoints principales

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/v1/health` | Salud de API y conexión a base de datos |
| GET | `/api/v1/stats/overview` | Resumen para el dashboard, con filtros |
| GET | `/api/v1/stats/technologies` | Ranking y métricas de tecnologías |
| GET | `/api/v1/stats/categories` | Demanda por categoría |
| GET | `/api/v1/stats/data-quality` | Puntaje e incidencias de calidad |
| GET | `/api/v1/recommendations` | Rutas de aprendizaje sugeridas |

La documentación completa y los esquemas de respuesta están disponibles en `/docs`.

## Pruebas y calidad

Backend:

```powershell
cd backend
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

Frontend:

```powershell
cd frontend
npm run lint
npm run build
```

El repositorio incluye **16 pruebas unitarias y de integración** para servicios, esquemas y contratos de API. El workflow de GitHub Actions ejecuta lint, formato, compilación, migraciones, pruebas y build en cada `push` y `pull_request`.

## Datos

El repositorio incluye un CSV de ejemplo en `data/seeds/sample_postings.csv`. Los datasets reales se guardan localmente en `data/raw/`, que está excluido del control de versiones.

No incluir datos personales de reclutadores o postulantes. Solo deben utilizarse campos públicos relacionados con la oferta: cargo, empresa, ubicación, modalidad, seniority, descripción resumida, tecnologías, salario publicado y fechas disponibles.

## Limitaciones actuales

- La demo pública usa datos simulados; no representa estadísticas oficiales del mercado chileno.
- El dataset real debe curarse e importarse localmente.
- La extracción de tecnologías y las recomendaciones son reglas heurísticas, no modelos predictivos.
- La API real todavía no está desplegada con una base de datos administrada.

## Roadmap

- [ ] Desplegar FastAPI y PostgreSQL administrado.
- [ ] Versionar snapshots anónimos del dataset y documentar su procedencia.
- [ ] Normalizar monedas y rangos salariales.
- [ ] Añadir filtros por rango de fechas y modalidad.
- [ ] Incorporar análisis de coocurrencia de tecnologías.
- [ ] Agregar pruebas de frontend y cobertura de backend.
- [ ] Publicar un informe mensual reproducible.

## Autor

**Ignacio Silva**  
Estudiante de Ingeniería en Informática, mención Ciencia de Datos.  
GitHub: https://github.com/yvvvl
