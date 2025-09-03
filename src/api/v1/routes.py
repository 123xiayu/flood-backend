from fastapi import APIRouter
from .endpoints import health, weather

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(weather.router, prefix="", tags=["weather"])
