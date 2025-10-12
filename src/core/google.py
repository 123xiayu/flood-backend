
"""
Google Weather API Integration Module

This module provides functions to fetch weather data from Google's Weather API.
It includes support for hourly forecasts, daily forecasts, current conditions,
and historical weather data based on geographic coordinates.
"""

import requests
from src.core.config import settings

# Load Google API configuration from settings
api_key = settings.GOOGLE_API_KEY
base_url = settings.GOOGLE_BASE_URL


def fetch_google_hourly_forecast(coordinates):
    """
    Fetch hourly weather forecast from Google Weather API.

    Retrieves detailed hourly forecast data for the specified coordinates
    using Google's Weather API service.

    Args:
        coordinates (tuple): Tuple containing (latitude, longitude) as floats

    Returns:
        dict: JSON response from Google Weather API containing hourly forecast data
        Exception: If an error occurs during the API request

    Note:
        Returns error dict with code 1 if GOOGLE_API_KEY is not configured
    """
    try:
        lat, lon = coordinates
        if not api_key:
            return {"code": 1, "message": "GOOGLE_API_KEY not set in environment", "data": None}
        url = f"{base_url}forecast/hours:lookup?key={api_key}&location.latitude={lat}&location.longitude={lon}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        return e


def fetch_google_daily_forecast(coordinates):
    """
    Fetch daily weather forecast from Google Weather API.

    Retrieves daily forecast data for the specified coordinates using
    Google's Weather API service. Provides multi-day weather outlook.

    Args:
        coordinates (tuple): Tuple containing (latitude, longitude) as floats

    Returns:
        dict: JSON response from Google Weather API containing daily forecast data
        Exception: If an error occurs during the API request

    Note:
        Returns error dict with code 1 if GOOGLE_API_KEY is not configured
    """
    try:
        lat, lon = coordinates
        if not api_key:
            return {"code": 1, "message": "GOOGLE_API_KEY not set in environment", "data": None}
        url = f"{base_url}forecast/days:lookup?key={api_key}&location.latitude={lat}&location.longitude={lon}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        return e


def fetch_google_conditions(coordinates):
    """
    Fetch current weather conditions from Google Weather API.

    Retrieves real-time current weather conditions for the specified
    coordinates using Google's Weather API service.

    Args:
        coordinates (tuple): Tuple containing (latitude, longitude) as floats

    Returns:
        dict: JSON response from Google Weather API containing current conditions
        Exception: If an error occurs during the API request

    Note:
        Returns error dict with code 1 if GOOGLE_API_KEY is not configured
    """
    try:
        lat, lon = coordinates
        if not api_key:
            return {"code": 1, "message": "GOOGLE_API_KEY not set in environment", "data": None}
        url = f"{base_url}currentConditions:lookup?key={api_key}&location.latitude={lat}&location.longitude={lon}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        return e


def fetch_google_history(coordinates):
    """
    Fetch historical weather data from Google Weather API.

    Retrieves historical hourly weather data for the specified coordinates
    using Google's Weather API service. Useful for analysis and comparison.

    Args:
        coordinates (tuple): Tuple containing (latitude, longitude) as floats

    Returns:
        dict: JSON response from Google Weather API containing historical data
        Exception: If an error occurs during the API request

    Note:
        Returns error dict with code 1 if GOOGLE_API_KEY is not configured
    """
    try:
        lat, lon = coordinates
        if not api_key:
            return {"code": 1, "message": "GOOGLE_API_KEY not set in environment", "data": None}
        url = f"{base_url}history/hours:lookup?key={api_key}&location.latitude={lat}&location.longitude={lon}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        return e
