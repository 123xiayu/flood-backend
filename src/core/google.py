
import requests
from src.core.config import settings

api_key = settings.GOOGLE_API_KEY
base_url = settings.GOOGLE_BASE_URL


def fetch_google_hourly_forecast(coordinates):
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
