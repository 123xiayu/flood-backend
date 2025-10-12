
"""
Weather Forecast Endpoint Module

This module provides weather forecast API endpoints for the urban flooding backend.
It includes functionality for retrieving weather forecasts and current weather
conditions from the Bureau of Meteorology.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.core.bom import fetch_weather_observation
from src.core.bom import parse_forecast_for_station
from src.core.bom import fetch_bom_forecast_xml
from src.core.helpers import find_nearest_station
from src.core.auth import verify_token

router = APIRouter()


class WeatherRequest(BaseModel):
    """
    Request model for weather forecast endpoints.

    Attributes:
        lat (float): Latitude coordinate in decimal degrees
        lon (float): Longitude coordinate in decimal degrees
    """
    lat: float
    lon: float


@router.post("/forecast", tags=["forecast"])
def get_forecast(request: WeatherRequest, token: str = Depends(verify_token)):
    """
    Get weather forecast for specified coordinates.

    Retrieves detailed weather forecast data from the Bureau of Meteorology
    for the nearest weather station to the provided coordinates. Returns
    forecast periods with descriptions, conditions, and timing information.

    Args:
        request (WeatherRequest): Request containing latitude and longitude
        token (str): Authenticated user token (from Authorization header)

    Returns:
        dict: Response containing:
            - code (int): Status code (0 for success, 1 for error)
            - message (str): Status message
            - data: List of forecast period data or None if error
    """
    try:
        nearest_station = find_nearest_station(request.lat, request.lon)
        if not nearest_station:
            return {"code": 1, "message": "No weather station found", "data": None}
        xml_content = fetch_bom_forecast_xml()
        forecasts = parse_forecast_for_station(
            xml_content, nearest_station['AAC'])
        return {"code": 0, "message": "Success", "data": forecasts}
    except Exception as e:
        return {"code": 1, "message": f"Error: {str(e)}", "data": None}

# New endpoint: /weathercondition


@router.post("/weathercondition", tags=["weather"])
def get_weather_condition(request: WeatherRequest, token: str = Depends(verify_token)):
    """
    Get current weather condition summary for specified coordinates.

    Retrieves a simplified weather condition summary including the forecast
    précis (brief description) and icon code from the Bureau of Meteorology.
    This endpoint provides a quick overview of current weather conditions.

    Args:
        request (WeatherRequest): Request containing latitude and longitude
        token (str): Authenticated user token (from Authorization header)

    Returns:
        dict: Response containing:
            - code (int): Status code (0 for success, 1 for error)
            - message (str): Status message
            - data: Weather condition summary with précis and icon code
    """
    try:
        nearest_station = find_nearest_station(request.lat, request.lon)
        if not nearest_station:
            return {"code": 1, "message": "No weather station found", "data": None}
        # Get first precis and element (icon code) from forecast
        xml_content = fetch_bom_forecast_xml()
        forecasts = parse_forecast_for_station(
            xml_content, nearest_station['AAC'])
        precis = None
        forecast_icon_code = None
        if forecasts:
            precis = forecasts[0]['forecast'].get('precis')
            # Find the first 'element' tag value in the first forecast period
            # The 'element' tag is usually used for icon codes in BOM XML
            forecast_icon_code = forecasts[0]['forecast'].get('element')
        # Get temperature from weather observation
        observations = fetch_weather_observation(nearest_station)
        temperature = None
        if observations:
            temperature = observations[0].get('air_temp')
        return {
            "code": 0,
            "message": "Success",
            "data": {
                "precis": precis,
                "temperature": temperature,
                "forecast_icon_code": forecast_icon_code
            }
        }
    except Exception as e:
        return {"code": 1, "message": f"Error: {str(e)}", "data": None}
