"""Digital Twin API client utilities.

Currently provides a simple function to POST hard-coded coordinates and
rainfall event ID to an (as yet undecided) Digital Twin endpoint and
return the parsed JSON response. This will later be wired to accept
dynamic parameters from an internal API endpoint.
"""

from __future__ import annotations
from typing import Any, Dict, Optional
import json
import logging
import requests

from src.core.config import settings

dt_base_url = settings.DT_BASE_URL


def fetch_digital_twin_risk(
        lat: float | None = None,
        lon: float | None = None,
        rainfall_event_id: Optional[str] = None,
) -> Dict[str, Any]:
    """POST to Digital Twin risk endpoint and return JSON response.

    Parameters
    ----------
    lat, lon: Optional explicit coordinates. If None, defaults to the hard-coded
            development values currently required (-31.846050, 115.898611).
    rainfall_event_id: Optional rainfall event identifier. Defaults to "design_2yr".

    Returns
    -------
    dict: Parsed JSON from the Digital Twin service or an error structure.
    """

    url = f"{dt_base_url}risk/point"
    if rainfall_event_id is None:
        payload = {
            "lat": lat,
            "lon": lon,
        }
    else:
        payload = {
            "lat": lat,
            "lon": lon,
            "rainfall_event_id": rainfall_event_id,
        }

    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {settings.DT_API_TOKEN}'
    }

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return e


def post_user_report(
        IssueReport: Any
) -> Dict[str, Any]:
    """POST to Digital Twin report endpoint and return JSON response.

    Parameters
    ----------
    IssueReport: Report data structure containing issue details.

    Returns
    -------
    dict: Parsed JSON from the Digital Twin service or an error structure.
    """

    url = f"{dt_base_url}report"

    payload = IssueReport.dict()

    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {settings.DT_API_TOKEN}'
    }

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return e


__all__ = ["fetch_digital_twin_risk", "post_user_report"]

if __name__ == "__main__":  # Simple manual test harness
    logging.basicConfig(level=logging.INFO)
    result = fetch_digital_twin_risk()
    print(json.dumps(result, indent=2, default=str))
