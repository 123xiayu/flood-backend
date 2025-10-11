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
    print(
        f"🌊 [RISK ANALYSIS] Fetching flood risk data for coordinates: ({request.lat}, {request.lon})")
    if request.rainfall_event_id:
        print(
            f"📊 [RISK ANALYSIS] Using rainfall event: {request.rainfall_event_id}")
    try:
        result = fetch_digital_twin_risk(
            lat=request.lat,
            lon=request.lon,
            rainfall_event_id=request.rainfall_event_id,
        )

        # The core function currently returns either a dict (success) or an Exception instance on error
        if isinstance(result, Exception):
            print(f"❌ [RISK ANALYSIS] Digital Twin API error: {str(result)}")
            return {"code": 1, "message": f"Error: {str(result)}", "data": None}

        if not result:
            print(f"⚠️  [RISK ANALYSIS] No data returned from Digital Twin API")
            return {"code": 1, "message": "No data returned from Digital Twin API", "data": None}

        print(f"✅ [RISK ANALYSIS] Successfully retrieved risk assessment data")
        return {"code": 0, "message": "Success", "data": result}
    except Exception as e:  # Fallback safeguard
        print(f"❌ [RISK ANALYSIS] Unhandled error: {str(e)}")
        return {"code": 1, "message": f"Unhandled error: {str(e)}", "data": None}
