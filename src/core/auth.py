"""
Authentication Module

This module provides authentication functionality for the urban flooding
backend API using Bearer token authentication. It handles token validation
and provides security dependencies for FastAPI endpoints.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from src.core.config import settings

# HTTPBearer security scheme for token authentication
security = HTTPBearer()


def get_api_token() -> str:
    """
    Retrieve the configured API token from settings.

    Returns:
        str: The configured API token

    Raises:
        ValueError: If API_TOKEN is not configured in settings
    """
    token = settings.API_TOKEN
    if not token:
        raise ValueError("API_TOKEN is not configured")
    return token


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify the provided Bearer token against the configured API token.

    This function is used as a FastAPI dependency to protect endpoints
    that require authentication. It validates the Bearer token from the
    Authorization header.

    Args:
        credentials (HTTPAuthorizationCredentials): The Bearer token credentials
            from the Authorization header

    Returns:
        str: The validated token if authentication is successful

    Raises:
        HTTPException: If the token is invalid or doesn't match the configured token
    """
    token = credentials.credentials
    api_token = get_api_token()

    if token != api_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
