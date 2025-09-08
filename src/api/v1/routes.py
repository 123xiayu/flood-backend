from fastapi import APIRouter
from .endpoints import health, weather, forecast, warnings

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(weather.router, prefix="", tags=["weather"])
api_router.include_router(forecast.router, prefix="", tags=["forecast"])
api_router.include_router(warnings.router, prefix="", tags=["warnings"])

