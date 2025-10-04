from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

from src.core.digitaltwin import fetch_digital_twin_risk

router = APIRouter()


class RiskRequest(BaseModel):
    lat: float = Field(
        None, description="Latitude in decimal degrees")
    lon: float = Field(
        None, description="Longitude in decimal degrees")
    rainfall_event_id: Optional[str] = Field(
        None,
        description="Rainfall event identifier (e.g. design_2yr, design_10yr)."
    )


@router.post("/risk", tags=["risk"])
def get_risk(request: RiskRequest) -> Dict[str, Any]:
    try:
        result = fetch_digital_twin_risk(
            lat=request.lat,
            lon=request.lon,
            rainfall_event_id=request.rainfall_event_id,
        )

        # The core function currently returns either a dict (success) or an Exception instance on error
        if isinstance(result, Exception):
            return {"code": 1, "message": f"Error: {str(result)}", "data": None}

        if not result:
            return {"code": 1, "message": "No data returned from Digital Twin API", "data": None}

        return {"code": 0, "message": "Success", "data": result}
    except Exception as e:  # Fallback safeguard
        return {"code": 1, "message": f"Unhandled error: {str(e)}", "data": None}
