from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

from src.core.digitaltwin import post_user_report

router = APIRouter()


class IssueReport(BaseModel):
    issue_type: str = Field(..., description="Type of the reported issue")
    description: Optional[str] = Field(
        None, description="Description of the issue")
    location: Dict[str, float] = Field(...,
                                       description="Location with latitude and longitude")
    user: Dict[str, str] = Field(
        ..., description="User information with uid, display_name, and email")


@router.post("/report", tags=["report"])
def get_risk(request: IssueReport) -> Dict[str, Any]:
    try:
        result = post_user_report(
            IssueReport=request
        )

        # The core function currently returns either a dict (success) or an Exception instance on error
        if isinstance(result, Exception):
            return {"code": 1, "message": f"Error: {str(result)}", "data": None}

        if not result:
            return {"code": 1, "message": "No data returned from Digital Twin API", "data": None}

        return {"code": 0, "message": "Success", "data": result}
    except Exception as e:  # Fallback safeguard
        print(e)
        return {"code": 1, "message": f"Unhandled error: {str(e)}", "data": None}
