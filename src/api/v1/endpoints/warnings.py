import requests
import feedparser
import re
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from src.core.helpers import find_nearest_station, calculate_distance
from src.core.auth import verify_token

router = APIRouter()


class WarningsRequest(BaseModel):
    lat: float
    lon: float
    radius_km: Optional[float] = 100.0
    fetch_details: Optional[bool] = True


def fetch_warning_details(url: str) -> Dict[str, Any]:
    """Fetch and parse detailed warning content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"error": f"Failed to fetch details: HTTP {response.status_code}"}

        soup = BeautifulSoup(response.content, 'lxml')

        details = {}

        product_content = soup.find('div', {'class': 'product'})
        if not product_content:
            product_content = soup.find('div', {'id': 'content'})
        if not product_content:
            product_content = soup.find('pre')

        if product_content:
            # Extract text content
            text = product_content.get_text(separator='\n', strip=True)
            details['full_text'] = text

            # Try to extract specific warning details
            lines = text.split('\n')

            # Extract warning type
            for line in lines[:5]:
                if 'WARNING' in line.upper() or 'WEATHER' in line.upper():
                    details['warning_type'] = line.strip()
                    break

            # Extract location/area
            area_pattern = r'for\s+(.+?)(?:\.|$)'
            for line in lines:
                match = re.search(area_pattern, line, re.IGNORECASE)
                if match:
                    details['affected_areas'] = match.group(1).strip()
                    break

            # Extract issue time
            time_pattern = r'Issued at (\d+:\d+\s+\w+\s+\w+)'
            for line in lines:
                match = re.search(time_pattern, line)
                if match:
                    details['issue_time'] = match.group(1)
                    break

            # Extract warning level/severity
            if 'SEVERE' in text.upper():
                details['severity'] = 'Severe'
            elif 'MODERATE' in text.upper():
                details['severity'] = 'Moderate'
            elif 'MINOR' in text.upper():
                details['severity'] = 'Minor'
            else:
                details['severity'] = 'Standard'

            # Extract next issue time if available
            next_pattern = r'Next issue[:\s]+(.+?)(?:\.|$)'
            for line in lines:
                match = re.search(next_pattern, line, re.IGNORECASE)
                if match:
                    details['next_issue'] = match.group(1).strip()
                    break

            # Extract warning message/summary
            warning_msg_start = ['WEATHER SITUATION:',
                                 'WARNING:', 'FORECAST:', 'SITUATION:']
            for start_phrase in warning_msg_start:
                if start_phrase in text:
                    idx = text.index(start_phrase)
                    # Get next 500 characters or until next section
                    msg = text[idx:idx+500].split('\n\n')[0]
                    details['warning_message'] = msg
                    break

        return details

    except Exception as e:
        return {"error": f"Failed to parse details: {str(e)}"}


def fetch_warnings_rss() -> Dict[str, Any]:
    """Fetch weather warnings RSS feed from BOM for Western Australia"""
    # Western Australia RSS feeds
    urls = [
        "https://www.bom.gov.au/fwo/IDZ00060.warnings_wa.xml",  # All WA warnings
        "https://www.bom.gov.au/fwo/IDZ00059.warnings_land_wa.xml",  # Land warnings
        "https://www.bom.gov.au/fwo/IDZ00058.warnings_marine_wa.xml",  # Marine warnings
        "http://www.bom.gov.au/fwo/IDZ00060.warnings_wa.xml"  # HTTP fallback
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    for url in urls:
        try:
            # Try with feedparser first
            feed = feedparser.parse(url)
            if feed.entries:
                return {"feed": feed, "url": url}

            # Try with requests if feedparser doesn't work
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    return {"feed": feed, "url": url}
        except Exception as e:
            continue

    # Return empty feed if all attempts fail
    return {"feed": {"entries": []}, "url": None}


def parse_warnings_feed(feed_data: Dict[str, Any], fetch_details: bool = False) -> List[Dict[str, Any]]:
    """Parse RSS feed and extract warning information"""
    feed = feed_data["feed"]
    warnings = []

    # Check if feed has entries attribute
    if not hasattr(feed, 'entries'):
        return warnings

    for entry in feed.entries:
        warning = {
            "title": entry.get("title", "").strip(),
            "description": entry.get("description", entry.get("summary", "")),
            "link": entry.get("link", ""),
            "pub_date": entry.get("published", ""),
            "category": entry.get("category", ""),
            "guid": entry.get("id", entry.get("guid", "")),
        }

        # Clean up title (remove extra whitespace and newlines)
        warning["title"] = ' '.join(warning["title"].split())

        # Try to parse the publication date
        if warning["pub_date"]:
            try:
                pub_date_parsed = entry.get("published_parsed")
                if pub_date_parsed:
                    warning["pub_date_parsed"] = datetime(
                        *pub_date_parsed[:6]).isoformat()
                else:
                    warning["pub_date_parsed"] = None
            except:
                warning["pub_date_parsed"] = None

        # Extract warning type from title
        title_lower = warning["title"].lower()
        if "marine" in title_lower:
            warning["type"] = "Marine"
        elif "severe weather" in title_lower:
            warning["type"] = "Severe Weather"
        elif "fire" in title_lower:
            warning["type"] = "Fire Weather"
        elif "sheep" in title_lower:
            warning["type"] = "Agricultural"
        elif "flood" in title_lower:
            warning["type"] = "Flood"
        elif "cyclone" in title_lower:
            warning["type"] = "Tropical Cyclone"
        else:
            warning["type"] = "General"

        # Fetch detailed content if requested
        if fetch_details and warning["link"]:
            warning["details"] = fetch_warning_details(warning["link"])

        warnings.append(warning)

    return warnings


def filter_warnings_by_location(warnings: List[Dict[str, Any]], lat: float, lon: float, radius_km: float) -> List[Dict[str, Any]]:
    """
    Filter warnings based on location radius.
    Note: This is a basic implementation that returns all warnings with location context.
    For more accurate filtering, we would need specific location data for each warning.
    """

    # Get nearest station for reference
    nearest_station = find_nearest_station(lat, lon)

    # Add location context to all warnings
    filtered_warnings = []
    for warning in warnings:
        # Add location context
        warning_with_location = warning.copy()
        warning_with_location["request_location"] = {
            "lat": lat,
            "lon": lon,
            "radius_km": radius_km
        }

        if nearest_station:
            warning_with_location["nearest_station"] = {
                "name": nearest_station["name"],
                "distance_km": calculate_distance(lat, lon, nearest_station["lat"], nearest_station["lon"])
            }

        filtered_warnings.append(warning_with_location)

    return filtered_warnings


@router.post("/warnings", tags=["warnings"])
def get_weather_warnings(request: WarningsRequest, token: str = Depends(verify_token)):
    """
    Get weather warnings for a specific location within a radius.
    Returns all active weather warnings from BOM RSS feed with optional detailed content.
    """
    print(
        f"[WARNINGS] Fetching weather warnings for coordinates: ({request.lat}, {request.lon})")
    print(
        f"[WARNINGS] Search radius: {request.radius_km} km, Fetch details: {request.fetch_details}")
    try:
        feed_data = fetch_warnings_rss()

        # Parse warnings with optional details
        all_warnings = parse_warnings_feed(
            feed_data, fetch_details=request.fetch_details or False)

        # Filter by location (basic implementation for now)
        filtered_warnings = filter_warnings_by_location(
            all_warnings,
            request.lat,
            request.lon,
            request.radius_km or 100.0
        )

        # Get nearest station info for context
        nearest_station = find_nearest_station(request.lat, request.lon)
        print(
            f"[WARNINGS] Found {len(filtered_warnings)} warnings in the area")

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "location": {
                    "lat": request.lat,
                    "lon": request.lon,
                    "radius_km": request.radius_km
                },
                "nearest_station": {
                    "name": nearest_station["name"] if nearest_station else None,
                    "station_id": nearest_station["station_id"] if nearest_station else None,
                    "lat": nearest_station["lat"] if nearest_station else None,
                    "lon": nearest_station["lon"] if nearest_station else None
                } if nearest_station else None,
                "total_warnings": len(filtered_warnings),
                "warnings": filtered_warnings,
                "feed_info": {
                    "source": "Bureau of Meteorology - Western Australia",
                    "url": feed_data["url"],
                    "details_fetched": request.fetch_details
                }
            }
        }

    except Exception as e:
        print(f"[WARNINGS] Error occurred: {str(e)}")
        return {
            "code": 1,
            "message": f"Error: {str(e)}",
            "data": None
        }


@router.get("/warnings/all", tags=["warnings"])
def get_all_weather_warnings(fetch_details: bool = True, token: str = Depends(verify_token)):
    """
    Get all weather warnings without location filtering.
    Returns all active weather warnings from BOM RSS feed with optional detailed content.

    Query parameters:
    - fetch_details: Whether to fetch detailed content from each warning URL (default: True)
    """
    print(f"[ALL WARNINGS] Fetching all weather warnings from BOM")
    print(f"[ALL WARNINGS] Fetch details: {fetch_details}")
    try:
        # Fetch RSS feed
        print(f"[ALL WARNINGS] Connecting to BOM RSS feed...")
        feed_data = fetch_warnings_rss()

        # Parse warnings with details
        print(f"[ALL WARNINGS] Parsing RSS feed data...")
        all_warnings = parse_warnings_feed(
            feed_data, fetch_details=fetch_details)
        print(f"[ALL WARNINGS] Found {len(all_warnings)} total warnings")

        return {
            "code": 0,
            "message": "Success",
            "data": {
                "total_warnings": len(all_warnings),
                "warnings": all_warnings,
                "feed_info": {
                    "source": "Bureau of Meteorology - Western Australia",
                    "url": feed_data["url"],
                    "details_fetched": fetch_details
                }
            }
        }

    except Exception as e:
        print(f"[ALL WARNINGS] Error occurred: {str(e)}")
        return {
            "code": 1,
            "message": f"Error: {str(e)}",
            "data": None
        }
