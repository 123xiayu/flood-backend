"""
Urban Flooding Backend API

Main application module for the urban flooding digital twin backend service.
This FastAPI application provides weather data, forecasts, warnings, and risk 
assessments to support flood monitoring and prediction systems.
"""

from src.api.v1.routes import api_router
from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Sets up the main FastAPI application with the API router and configures
    the application title. All API routes are prefixed with /api/v1.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(title="flood-backend")
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8118)
