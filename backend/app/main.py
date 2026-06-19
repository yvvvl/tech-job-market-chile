from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.health import router as health_router
from app.routers.recommendations import router as recommendations_router
from app.routers.stats import router as stats_router
from app.schemas.common import RootResponse

app = FastAPI(
    title=settings.app_name,
    description="API para analizar ofertas laborales TI en Chile.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(stats_router)
app.include_router(recommendations_router)


@app.get(
    "/",
    response_model=RootResponse,
)
def root() -> RootResponse:
    return RootResponse(
        message="Tech Job Market Intelligence Chile API",
        docs="/docs",
        health="/api/v1/health",
        overview="/api/v1/stats/overview",
    )
