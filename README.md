# Tech Job Market Intelligence Chile
[![CI](https://github.com/yvvvl/tech-job-market-chile/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/yvvvl/tech-job-market-chile/actions/workflows/ci.yml)

Demo pública: https://tech-job-market-chile-demo.silva-ignacio-696.workers.dev/

Plataforma de análisis del mercado laboral TI en Chile. El proyecto procesa ofertas laborales desde archivos CSV curados, extrae tecnologías, clasifica cargos por seniority/categoría y expone métricas mediante una API REST y un dashboard web.

El objetivo es responder preguntas como:

- Qué tecnologías se piden más en cargos TI en Chile.
- Qué tecnologías aparecen con más frecuencia en ofertas junior o trainee.
- Qué perfiles tienen mayor demanda: backend, frontend, data, DevOps, QA o soporte.
- Qué rutas de aprendizaje conviene priorizar según el mercado.
- Cómo evoluciona un dataset real de ofertas laborales cuando se actualiza periódicamente.

Este proyecto está pensado como portafolio técnico para demostrar habilidades en desarrollo backend, análisis de datos, frontend, bases de datos, modelado relacional e integración de APIs.

---

## Estado del proyecto

Estado actual: MVP funcional.

La demo pública usa datos simulados para mantenerse disponible de forma gratuita. El backend real está implementado con FastAPI, PostgreSQL, Alembic, tests y CI.

El proyecto actualmente permite:

- Levantar PostgreSQL con Docker.
- Importar ofertas laborales desde CSV.
- Validar el CSV antes de importarlo.
- Guardar empresas, ofertas y tecnologías en PostgreSQL.
- Exponer métricas desde FastAPI.
- Consumir la API desde un frontend React.
- Visualizar estadísticas en Dashboard, Technology Explorer y Career Recommendations.
- Probar endpoints desde Bruno o desde la documentación automática de FastAPI.

---
## Vista del producto

### Dashboard del mercado laboral

El panel resume ofertas, empresas, tecnologías, ciudades, seniority y distribución salarial a partir del dataset importado.

![Dashboard general](docs/images/dashboard-overview.png)

![Analítica del dashboard](docs/images/dashboard-analytics.png)

### Explorador de tecnologías

Permite consultar demanda, accesibilidad para perfiles junior, tecnologías relacionadas y métricas asociadas a cada skill.

![Explorador de tecnologías](docs/images/technology-explorer.png)

### Rutas de aprendizaje

Genera rutas de carrera basadas en la demanda observada dentro del dataset.

![Rutas de aprendizaje](docs/images/career-recommendations.png)

<details>
<summary>API y validación técnica</summary>

### Documentación OpenAPI

![Documentación de la API](docs/images/api-documentation.png)

### Pruebas con Bruno

![Respuesta del endpoint overview](docs/images/bruno-overview.png)

![Endpoint de calidad de datos](docs/images/bruno-data-quality.png)

</details>


## Stack técnico

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg2
- python-dotenv
- Uvicorn

### Frontend

- React
- TypeScript
- Vite
- TanStack Router
- React Query
- TailwindCSS
- shadcn/ui
- Recharts

### Infraestructura local

- Docker
- Docker Compose
- PostgreSQL 16
- Adminer

### Herramientas de desarrollo

- VS Code
- Bruno
- Git / GitHub
- PowerShell

---

## Arquitectura general

```txt
tech-job-market-chile/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── database/
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── pipeline/
│   │   │   └── tech_rules.py
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── stats.py
│   │   │   └── recommendations.py
│   │   └── scripts/
│   │       ├── init_db.py
│   │       ├── reset_db.py
│   │       ├── seed_data.py
│   │       ├── import_csv.py
│   │       └── validate_csv.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   └── api/
│   │   │       └── market.ts
│   │   └── routes/
│   │       ├── dashboard.tsx
│   │       ├── explorer.tsx
│   │       └── recommendations.tsx
│   └── package.json
│
├── data/
│   ├── raw/
│   │   └── ofertas_ti_chile_2026_06.csv
│   └── seeds/
│       └── sample_postings.csv
│
├── scripts/
│   └── import-real-data.ps1
│
├── docker-compose.yml
├── .env.example
└── README.md
````

---

## Flujo de datos

```txt
CSV real
   ↓
validate_csv.py
   ↓
import_csv.py
   ↓
PostgreSQL
   ↓
FastAPI
   ↓
React Dashboard
```

El sistema no depende de scraping automático. La fuente principal de datos es un CSV curado manualmente a partir de ofertas públicas. Esto permite mantener control sobre la calidad, trazabilidad y legalidad del dataset.

---

## Modelo de datos

El modelo relacional principal está compuesto por:

### companies

Empresas que publican ofertas.

Campos principales:

* id
* name
* created_at

### job_postings

Ofertas laborales.

Campos principales:

* id
* title
* company_id
* source
* source_url
* city
* region
* modality
* seniority
* category
* description
* salary_min
* salary_max
* salary_currency
* published_at
* collected_at
* created_at

### technologies

Tecnologías detectadas en las ofertas.

Campos principales:

* id
* name
* category
* created_at

### job_posting_technologies

Tabla intermedia muchos-a-muchos entre ofertas y tecnologías.

Campos principales:

* id
* job_posting_id
* technology_id

---

## CSV de entrada

El importador espera un CSV con estas columnas:

```csv
source,source_url,title,company,city,region,modality,seniority,category,description,technologies_raw,salary_min,salary_max,salary_currency,published_at,collected_at
```

Ejemplo:

```csv
source,source_url,title,company,city,region,modality,seniority,category,description,technologies_raw,salary_min,salary_max,salary_currency,published_at,collected_at
GetOnBoard,https://www.example.com/job,Junior Front-end Engineer,Empresa Demo,Santiago,Metropolitana,Hibrido,junior,Frontend,"Desarrollo frontend con React, TypeScript y consumo de APIs.","React; TypeScript; JavaScript; APIs",1300,2400,USD,2026-06-17,2026-06-17
```

Notas importantes:

* Si un campo contiene comas, debe ir entre comillas dobles.
* Si una oferta no tiene salario, los campos `salary_min` y `salary_max` pueden quedar vacíos.
* Si no se conoce el seniority, usar `unknown`.
* Si no se conoce la modalidad, usar `unknown`.
* `collected_at` es obligatorio.
* `published_at` puede quedar vacío si la plataforma no entrega fecha exacta.

---

## Instalación local

### 1. Clonar repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
cd tech-job-market-chile
```

### 2. Crear entorno virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias del backend

```powershell
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

### 4. Instalar dependencias del frontend

```powershell
cd frontend
npm install
cd ..
```

---

## Variables de entorno

### Backend

Crear archivo:

```txt
backend/.env
```

Contenido:

```env
DATABASE_URL=postgresql+psycopg2://techuser:techpass@localhost:5433/tech_jobs_chile
FRONTEND_URL=http://localhost:5173
```

### Frontend

Crear archivo:

```txt
frontend/.env.local
```

Contenido:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## Levantar servicios

### 1. Levantar PostgreSQL y Adminer

Desde la raíz:

```powershell
docker compose up -d
```

Verificar:

```powershell
docker ps
```

Servicios esperados:

```txt
tech_jobs_postgres
tech_jobs_adminer
```

URLs locales:

```txt
PostgreSQL: localhost:5433
Adminer:    http://localhost:8080
```

Credenciales de Adminer:

```txt
Sistema: PostgreSQL
Servidor: postgres
Usuario: techuser
Contraseña: techpass
Base de datos: tech_jobs_chile
```

---

## Importar datos

### Validar CSV

Desde `backend`:

```powershell
cd backend
python -m app.scripts.validate_csv ..\data\raw\ofertas_ti_chile_2026_06.csv
```

El CSV está listo para importar si el validador muestra:

```txt
Errores: 0
CSV válido para importar.
```

### Importar CSV real

Desde `backend`:

```powershell
python -m app.scripts.reset_db
python -m app.scripts.import_csv ..\data\raw\ofertas_ti_chile_2026_06.csv --replace
```

También se puede usar el script desde la raíz:

```powershell
.\scripts\import-real-data.ps1
```

Este script valida el CSV, resetea la base e importa el dataset real.

---

## Levantar backend

Desde `backend`:

```powershell
python -m uvicorn app.main:app --reload
```

URLs principales:

```txt
API:  http://localhost:8000
Docs: http://localhost:8000/docs
```

---

## Levantar frontend

Desde `frontend`:

```powershell
npm run dev
```

URL local:

```txt
http://localhost:5173
```

Rutas principales:

```txt
http://localhost:5173/dashboard
http://localhost:5173/explorer
http://localhost:5173/recommendations
```

---

## Endpoints de la API

Base URL:

```txt
http://localhost:8000/api/v1
```

| Método | Endpoint              | Descripción                                                      |
| ------ | --------------------- | ---------------------------------------------------------------- |
| GET    | `/health`             | Estado de la API, conexión a base de datos y conteos principales |
| GET    | `/stats/overview`     | Métricas generales para el dashboard                             |
| GET    | `/stats/technologies` | Ranking de tecnologías detectadas                                |
| GET    | `/stats/cities`       | Distribución de ofertas por ciudad                               |
| GET    | `/stats/seniority`    | Distribución por seniority                                       |
| GET    | `/recommendations`    | Rutas de aprendizaje recomendadas                                |

Ejemplos:

```txt
GET http://localhost:8000/api/v1/health
GET http://localhost:8000/api/v1/stats/overview
GET http://localhost:8000/api/v1/stats/technologies
GET http://localhost:8000/api/v1/recommendations
```

---

## Pruebas con Bruno

Variables recomendadas:

```txt
baseUrl = http://localhost:8000
apiUrl = http://localhost:8000/api/v1
```

Requests sugeridas:

```txt
GET {{baseUrl}}/
GET {{apiUrl}}/health
GET {{apiUrl}}/stats/overview
GET {{apiUrl}}/stats/technologies
GET {{apiUrl}}/stats/cities
GET {{apiUrl}}/stats/seniority
GET {{apiUrl}}/recommendations
```

---

## Funcionalidades principales

### Dashboard

Muestra una vista general del dataset:

* Total de ofertas.
* Total de empresas.
* Total de tecnologías.
* Total de ciudades.
* Tendencia mensual.
* Tecnologías más demandadas.
* Distribución por categoría.
* Distribución por seniority.
* Distribución por ciudad.
* Rangos salariales disponibles.

### Technology Explorer

Permite explorar tecnologías detectadas en las ofertas:

* Demanda relativa.
* Categoría.
* Compatibilidad con perfiles junior.
* Salario promedio estimado cuando hay datos.
* Tecnologías relacionadas.
* Tendencia visual basada en el dataset.

### Career Recommendations

Genera rutas recomendadas a partir de las tecnologías presentes en la base:

* Frontend Engineer.
* Backend Engineer.
* Data Analyst.
* Cloud & DevOps.

Cada ruta incluye:

* Stack sugerido.
* Puntaje de demanda.
* Puntaje de entrada junior.
* Tiempo estimado de aprendizaje.
* Salario promedio estimado cuando hay datos.

---

## Decisiones técnicas

### CSV curado sobre scraping automático

El proyecto está diseñado para trabajar con CSVs curados manualmente. Esto permite:

* Mantener trazabilidad de la fuente.
* Evitar dependencia de endpoints privados o inestables.
* Revisar calidad de datos antes de importarlos.
* Evitar capturar información personal innecesaria.
* Construir un dataset defendible para portafolio.

### PostgreSQL sobre archivos planos

PostgreSQL permite modelar correctamente:

* Ofertas.
* Empresas.
* Tecnologías.
* Relaciones muchos-a-muchos.
* Consultas agregadas para métricas.

### FastAPI como capa de servicio

FastAPI permite:

* Documentación automática con OpenAPI.
* Endpoints simples para dashboard.
* Integración directa con frontend.
* Validación y evolución futura hacia una API más completa.

### React Query para consumo de API

React Query facilita:

* Fetching declarativo.
* Estados de carga.
* Manejo de errores.
* Cache en frontend.

---

## Limitaciones actuales

Este proyecto está en etapa MVP. Algunas limitaciones conocidas:

* El dataset todavía es pequeño y curado manualmente.
* Las métricas de salario deben interpretarse con cuidado si existen distintas monedas.
* No hay normalización completa de CLP, USD y UF a una moneda única.
* La extracción de tecnologías usa reglas, diccionario y parsing básico.
* El score de tendencia todavía es simple y puede mejorarse con más datos históricos.
* No hay autenticación porque la API es local y de lectura.
* No hay tests automatizados todavía.
* No se usa Alembic para migraciones; en desarrollo se usa reset de base.

---

## Roadmap

### Corto plazo

* Aumentar dataset a 100 ofertas reales.
* Crear colección Bruno dentro del repositorio.
* Mejorar normalización de tecnologías y aliases.
* Normalizar salarios por moneda.
* Agregar screenshots al README.
* Crear tests para validación CSV y extracción de tecnologías.

### Mediano plazo

* Agregar Alembic para migraciones.
* Separar capa de servicios y repositorios.
* Agregar filtros en API por seniority, categoría, ciudad y modalidad.
* Agregar endpoint para detalle de tecnología.
* Mejorar motor de recomendaciones.
* Agregar análisis de co-ocurrencia de stacks.

### Largo plazo

* Automatizar ingesta desde fuentes permitidas.
* Agregar dashboard administrativo.
* Agregar histórico mensual real.
* Crear despliegue público del frontend.
* Crear despliegue de API con base de datos administrada.
* Agregar CI con GitHub Actions.

---

## Comandos útiles

### Levantar base de datos

```powershell
docker compose up -d
```

### Validar CSV

```powershell
cd backend
python -m app.scripts.validate_csv ..\data\raw\ofertas_ti_chile_2026_06.csv
```

### Importar dataset real

```powershell
.\scripts\import-real-data.ps1
```

### Levantar backend

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

### Levantar frontend

```powershell
cd frontend
npm run dev
```

### Build frontend

```powershell
cd frontend
npm run build
```

---

## Buenas prácticas de datos

El dataset debe contener solo información relacionada con ofertas laborales.

No incluir:

* Correos personales.
* Teléfonos personales.
* Nombres de reclutadores.
* Información privada.
* Datos de postulantes.
* Información obtenida mediante login automatizado, tokens o cookies.

Sí incluir:

* Título de la oferta.
* Empresa.
* Fuente.
* URL pública.
* Ciudad.
* Modalidad.
* Seniority.
* Categoría.
* Descripción resumida.
* Tecnologías mencionadas.
* Rango salarial si aparece públicamente.
* Fecha de publicación si está disponible.
* Fecha de recolección.

---

## Autor

Ignacio Silva

Estudiante de Ingeniería Informática con mención en Ciencia de Datos.
Proyecto de portafolio orientado a desarrollo backend, análisis de datos, bases de datos y visualización de información del mercado laboral TI en Chile.
