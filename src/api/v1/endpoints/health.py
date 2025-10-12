"""
Health Check Endpoint Module

This module provides health check functionality for the urban flooding backend API.
It includes endpoints to monitor the API's operational status and availability.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health():
    """
    Health check endpoint.

    Returns the current operational status of the API. This endpoint can be
    used by monitoring systems, load balancers, and other services to verify
    that the API is running and responsive.

    Returns:
        dict: Simple status response indicating the API is operational
            {"status": "ok"}
    """
    return {"status": "ok"}
