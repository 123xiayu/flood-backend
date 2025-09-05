import math
import os
import json
from typing import Any, Dict, Optional


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def load_stations() -> Dict[str, Any]:
    """Load station data from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    station_file = os.path.join(current_dir, "../../data/station.json")
    try:
        with open(station_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"PerthStations": []}


def find_nearest_station(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Find the nearest weather station to given coordinates"""
    stations_data = load_stations()
    stations = stations_data.get("PerthStations", [])

    if not stations:
        return None

    nearest_station = None
    min_distance = float('inf')

    for station in stations:
        distance = calculate_distance(lat, lon, station['lat'], station['lon'])
        if distance < min_distance:
            min_distance = distance
            nearest_station = station

    return nearest_station