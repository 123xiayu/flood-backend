from fastapi import APIRouter
from .endpoints import health, weather, forecast, warnings, gweather, risk, report

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(weather.router, prefix="", tags=["weather"])
api_router.include_router(forecast.router, prefix="", tags=["forecast"])
api_router.include_router(warnings.router, prefix="", tags=["warnings"])
api_router.include_router(gweather.router, prefix="", tags=["google"])
api_router.include_router(risk.router, prefix="", tags=["risk"])
api_router.include_router(report.router, prefix="", tags=["report"])
