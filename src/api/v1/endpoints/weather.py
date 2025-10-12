"""
Weather Data Endpoint Module

This module provides weather-related API endpoints for the urban flooding backend.
It includes functionality for retrieving current weather observations and historical
weather data from the Bureau of Meteorology and other weather services.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
from pydantic import BaseModel
import requests
from datetime import datetime
import io
import pandas as pd

from src.core.helpers import find_nearest_station
from src.core.auth import verify_token

router = APIRouter()


def get_months_in_range(start_date: datetime, end_date: datetime) -> list:
    """
    Generate a list of month strings (YYYYMM format) for the given date range.

    Creates a list of all months between the start and end dates, inclusive,
    formatted as YYYYMM strings for use in historical weather data URLs.

    Args:
        start_date (datetime): Start date of the range
        end_date (datetime): End date of the range

    Returns:
        list: List of month strings in YYYYMM format (e.g., ["202301", "202302"])
    """
    months = []
    current = start_date.replace(day=1)

    while current <= end_date:
        months.append(current.strftime("%Y%m"))
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return months


def fetch_historical_data(station: Dict[str, Any], start_date: datetime, end_date: datetime) -> list:
    """
    Fetch historical weather data for a specific station within a date range.

    Downloads and processes historical weather data from the Bureau of Meteorology
    for the specified station and date range. Data is retrieved month by month
    using the station's historical data URL template.

    Args:
        station (Dict[str, Any]): Station information dictionary containing
            'history_url_template' and other station metadata
        start_date (datetime): Start date for historical data retrieval
        end_date (datetime): End date for historical data retrieval

    Returns:
        list: List of dictionaries containing processed historical weather data
    """
    months = get_months_in_range(start_date, end_date)
    all_data = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/csv,application/csv,text/plain,*/*',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    for month in months:
        url = station['history_url_template'].replace(
            'YYYYMM', month).replace('YYYYMM', month)

        try:
            response = requests.get(url, headers=headers, stream=True)

            if response.status_code == 200:
                try:
                    content = response.content.decode('utf-8', errors='ignore')
                    lines = content.split('\n')
                    header_line = None

                    for i, line in enumerate(lines):
                        if 'Date' in line and (',' in line or 'temperature' in line.lower()):
                            header_line = i
                            break
                        if i > 20:
                            break

                    if header_line is not None:
                        csv_content = '\n'.join(lines[header_line:])
                        df = pd.read_csv(io.StringIO(
                            csv_content), on_bad_lines='skip')

                        if not df.empty and 'Date' in df.columns:
                            df['Date'] = pd.to_datetime(
                                df['Date'], errors='coerce')
                            mask = (df['Date'] >= start_date) & (
                                df['Date'] <= end_date)
                            filtered_df = df[mask]

                            for _, row in filtered_df.iterrows():
                                cleaned_row = {}
                                for col, val in row.items():
                                    if pd.notna(val) and str(val).strip() != '':
                                        cleaned_row[col] = val
                                if cleaned_row:
                                    all_data.append(cleaned_row)

                except Exception as e:
                    continue

        except Exception as e:
            continue

    return all_data


class WeatherRequest(BaseModel):
    """
    Request model for current weather data endpoints.

    Attributes:
        lat (float): Latitude coordinate in decimal degrees
        lon (float): Longitude coordinate in decimal degrees
    """
    lat: float
    lon: float


class HistoricalWeatherRequest(BaseModel):
    """
    Request model for historical weather data endpoints.

    Attributes:
        lat (float): Latitude coordinate in decimal degrees
        lon (float): Longitude coordinate in decimal degrees
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    """
    lat: float
    lon: float
    start_date: str  # Format: "YYYY-MM-DD"
    end_date: str    # Format: "YYYY-MM-DD"


@router.post("/weather", tags=["weather"])
def get_weather(request: WeatherRequest, token: str = Depends(verify_token)):
    """
    Get current weather data for specified coordinates.

    Finds the nearest weather station to the provided coordinates and retrieves
    the latest weather observations from the Bureau of Meteorology. Returns
    comprehensive weather data including temperature, humidity, wind, and pressure.

    Args:
        request (WeatherRequest): Request containing latitude and longitude
        token (str): Authenticated user token (from Authorization header)

    Returns:
        dict: Response containing:
            - code (int): Status code (0 for success, 1 for error)
            - message (str): Status message
            - data: Weather observation data or None if error
            - station_info: Information about the weather station used
    """
    try:
        # Find nearest station
        nearest_station = find_nearest_station(request.lat, request.lon)

        if not nearest_station:
            return {
                "code": 1,
                "message": "No weather station found",
                "data": None
            }

        # Get weather data from BOM API
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(nearest_station['url'], headers=headers)

        if response.status_code != 200:
            return {
                "code": 1,
                "message": f"Failed to fetch weather data: HTTP {response.status_code}",
                "data": None
            }

        weather_data = response.json()

        # Extract data from the response
        if 'observations' not in weather_data or 'data' not in weather_data['observations']:
            return {
                "code": 1,
                "message": "Invalid weather data format",
                "data": None
            }

        observations = weather_data['observations']['data']

        # Filter and format the relevant data
        filtered_data = []
        for obs in observations:
            filtered_obs = {
                "station_name": obs.get("name"),
                "local_date_time": obs.get("local_date_time"),
                "local_date_time_full": obs.get("local_date_time_full"),
                "lat": obs.get("lat"),
                "lon": obs.get("lon"),
                "air_temp": obs.get("air_temp"),
                "apparent_t": obs.get("apparent_t"),
                "dewpt": obs.get("dewpt"),
                "rain_trace": obs.get("rain_trace"),
                "rel_hum": obs.get("rel_hum"),
                "wind_dir": obs.get("wind_dir"),
                "wind_spd_kmh": obs.get("wind_spd_kmh"),
                "gust_kmh": obs.get("gust_kmh"),
                "weather": obs.get("weather"),
                "cloud": obs.get("cloud"),
                "vis_km": obs.get("vis_km")
            }
            filtered_data.append(filtered_obs)

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "station_info": {
                    "name": nearest_station["name"],
                    "station_id": nearest_station["station_id"],
                    "lat": nearest_station["lat"],
                    "lon": nearest_station["lon"]
                },
                "observations": filtered_data
            }
        }

    except Exception as e:
        return {
            "code": 1,
            "message": f"Error: {str(e)}",
            "data": None
        }


@router.post("/weather/historical", tags=["weather"])
def get_historical_weather(request: HistoricalWeatherRequest, token: str = Depends(verify_token)):
    """
    Get historical weather data for specified coordinates and date range.

    Retrieves historical weather data from the Bureau of Meteorology for the
    nearest weather station to the provided coordinates. Data is fetched for
    the specified date range and processed from CSV files.

    Args:
        request (HistoricalWeatherRequest): Request containing coordinates and date range
        token (str): Authenticated user token (from Authorization header)

    Returns:
        dict: Response containing:
            - code (int): Status code (0 for success, 1 for error)
            - message (str): Status message
            - data: List of historical weather records or None if error
            - station_info: Information about the weather station used
            - date_range: The requested date range
    """
    try:
        # Parse dates
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")

        if start_date > end_date:
            return {
                "code": 1,
                "message": "Start date must be before or equal to end date",
                "data": None
            }

        # Find nearest station
        nearest_station = find_nearest_station(request.lat, request.lon)

        if not nearest_station:
            return {
                "code": 1,
                "message": "No weather station found",
                "data": None
            }

        # Fetch historical data
        historical_data = fetch_historical_data(
            nearest_station, start_date, end_date)

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "station_info": {
                    "name": nearest_station["name"],
                    "station_id": nearest_station["station_id"],
                    "lat": nearest_station["lat"],
                    "lon": nearest_station["lon"]
                },
                "date_range": {
                    "start_date": request.start_date,
                    "end_date": request.end_date
                },
                "records_count": len(historical_data),
                "historical_data": historical_data
            }
        }

    except ValueError as e:
        return {
            "code": 1,
            "message": f"Invalid date format. Use YYYY-MM-DD format: {str(e)}",
            "data": None
        }
    except Exception as e:
        return {
            "code": 1,
            "message": f"Error: {str(e)}",
            "data": None
        }
