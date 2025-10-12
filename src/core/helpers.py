"""
Helper Utilities Module

This module provides utility functions for the urban flooding backend,
including distance calculations, weather station management, and
geographic data processing functions.
"""

import math
import os
import json
from typing import Any, Dict, Optional


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points using the Haversine formula.

    This function calculates the shortest distance over the earth's surface
    between two points specified by their latitude and longitude coordinates.

    Args:
        lat1 (float): Latitude of the first point in decimal degrees
        lon1 (float): Longitude of the first point in decimal degrees
        lat2 (float): Latitude of the second point in decimal degrees
        lon2 (float): Longitude of the second point in decimal degrees

    Returns:
        float: Distance between the two points in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def load_stations() -> Dict[str, Any]:
    """
    Load weather station data from the stations JSON configuration file.

    Reads the station configuration from data/station.json which contains
    information about weather stations including their coordinates, IDs,
    and API endpoints.

    Returns:
        Dict[str, Any]: Dictionary containing station data with structure:
            {"PerthStations": [list of station dictionaries]}
            Returns empty PerthStations list if file is not found
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    station_file = os.path.join(current_dir, "../../data/station.json")
    try:
        with open(station_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"PerthStations": []}


def find_nearest_station(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """
    Find the nearest weather station to the given coordinates.

    Searches through all available weather stations to find the one
    closest to the specified latitude and longitude coordinates using
    the Haversine distance formula.

    Args:
        lat (float): Target latitude in decimal degrees
        lon (float): Target longitude in decimal degrees

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing the nearest station
            information including name, station_id, coordinates, and API URLs.
            Returns None if no stations are available.
    """
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
