"""
API Version 1 Routes Module

This module configures the main API router for version 1 of the urban flooding
backend API. It combines all endpoint routers and organizes them with appropriate
tags for API documentation and logical grouping.
"""

from fastapi import APIRouter
from .endpoints import health, weather, forecast, warnings, gweather, risk, report

# Main API router for version 1
api_router = APIRouter()

# Include all endpoint routers with their respective tags
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(weather.router, prefix="", tags=["weather"])
api_router.include_router(forecast.router, prefix="", tags=["forecast"])
api_router.include_router(warnings.router, prefix="", tags=["warnings"])
api_router.include_router(gweather.router, prefix="", tags=["google"])
api_router.include_router(risk.router, prefix="", tags=["risk"])
api_router.include_router(report.router, prefix="", tags=["report"])
