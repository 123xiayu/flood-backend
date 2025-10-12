"""
Issue Reporting Endpoint Module

This module provides issue reporting API endpoints for the urban flooding backend.
It allows users to submit reports about flooding, infrastructure issues, or other
concerns directly to the digital twin platform for processing and response.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

from src.core.digitaltwin import post_user_report

router = APIRouter()


class IssueReport(BaseModel):
    """
    Request model for issue reporting endpoints.

    Attributes:
        issue_type (str): Type/category of the reported issue
        description (Optional[str]): Detailed description of the issue
        location (Dict[str, float]): Dictionary containing latitude and longitude coordinates
        user (Dict[str, str]): User information including uid, display_name, and email
    """
    issue_type: str = Field(..., description="Type of the reported issue")
    description: Optional[str] = Field(
        None, description="Description of the issue")
    location: Dict[str, float] = Field(...,
                                       description="Location with latitude and longitude")
    user: Dict[str, str] = Field(
        ..., description="User information with uid, display_name, and email")


@router.post("/report", tags=["report"])
def submit_issue_report(request: IssueReport) -> Dict[str, Any]:
    """
    Submit an issue report to the digital twin platform.

    Accepts user-submitted issue reports containing details about flooding,
    infrastructure problems, or other concerns. The report is forwarded to
    the digital twin platform for processing, analysis, and appropriate response.

    Args:
        request (IssueReport): Issue report containing type, description, location, and user info

    Returns:
        Dict[str, Any]: Response containing:
            - code (int): Status code (0 for success, 1 for error)
            - message (str): Status message
            - data: Report submission confirmation or None if error
    """
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
