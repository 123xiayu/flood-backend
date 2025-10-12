"""
Bureau of Meteorology (BOM) Integration Module

This module provides functions to fetch and parse weather data from the
Australian Bureau of Meteorology. It handles weather observations and
forecast data retrieval from BOM's public APIs.
"""

import xml.etree.ElementTree as ET
import requests


def fetch_weather_observation(station):
    """
    Fetch current weather observations for a specific weather station.

    Retrieves the latest weather observation data from the Bureau of
    Meteorology for the specified station. Includes proper headers to
    avoid 403 responses from the BOM servers.

    Args:
            station (dict): Dictionary containing station information including 'url'
                    key with the BOM API endpoint URL

    Returns:
            list: List of weather observation data from the station

    Raises:
            Exception: If the HTTP request fails or the response format is invalid
    """
    # Use proper User-Agent header to avoid 403 from bom.gov.au
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(station['url'], headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch weather data: HTTP {response.status_code}")
    weather_data = response.json()
    if 'observations' not in weather_data or 'data' not in weather_data['observations']:
        raise Exception("Invalid weather data format")
    observations = weather_data['observations']['data']
    return observations


def parse_forecast_for_station(xml_content, aac):
    """
    Parse BOM forecast XML data for a specific area administrative code (AAC).

    Processes the XML forecast data from the Bureau of Meteorology and extracts
    forecast information for the specified area. The AAC is used to filter
    forecasts to a specific geographic area.

    Args:
            xml_content (str): Raw XML content from BOM forecast API
            aac (str): Area Administrative Code to filter forecasts for

    Returns:
            list: List of forecast dictionaries containing:
                    - area: Area name/description
                    - start_time: Forecast period start time
                    - end_time: Forecast period end time  
                    - forecast: Dictionary of forecast elements and text
    """
    root = ET.fromstring(xml_content)
    forecasts = []
    for area in root.findall(".//area"):
        if area.attrib.get("aac", "") != aac:
            continue
        area_name = area.attrib.get("description", "")
        for period in area.findall("forecast-period"):
            period_data = {
                "area": area_name,
                "start_time": period.attrib.get("start-time-local", ""),
                "end_time": period.attrib.get("end-time-local", ""),
                "forecast": {}
            }
            for elem in period:
                if elem.tag == "text":
                    period_data["forecast"][elem.attrib.get(
                        "type", "text")] = elem.text
                else:
                    period_data["forecast"][elem.tag] = elem.text
            forecasts.append(period_data)
    return forecasts


def fetch_bom_forecast_xml():
    """
    Fetch forecast XML data from the Bureau of Meteorology.

    Retrieves the raw XML forecast data from BOM's forecast service.
    This data contains detailed weather forecasts for various areas
    across Australia and can be parsed using parse_forecast_for_station().

    Returns:
            bytes: Raw XML content from the BOM forecast API

    Raises:
            Exception: If the HTTP request fails (non-200 status code)
    """
    url = "http://www.bom.gov.au/fwo/IDW14199.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch forecast data: HTTP {response.status_code}")
    return response.content
