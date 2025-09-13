from fastapi import APIRouter
from pydantic import BaseModel
from core.google import fetch_google_conditions

router = APIRouter()

class WeatherRequest(BaseModel):
	lat: float
	lon: float


@router.post("/google/conditions", tags=["gweather"])
def get_google_conditions(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_conditions(coordinates)
		if not data:
			return {"code": 1, "message": "No data returned from Google Weather API", "data": None}
		
		weatherCondition = 	data.get("weatherCondition")
		condition = weatherCondition['description']['text']
		forecast_icon_uri = weatherCondition['iconBaseUri'] 
		
		temp = data.get("temperature")['degrees'] 
		feels_like = data.get("feelsLikeTemperature")['degrees'] 

		return {"code": 0, "message": "Success", "data": 
		  {
			"condition": condition,
			"temperature": temp,
			"feels_like": feels_like,
			"forecast_icon_uri": forecast_icon_uri
			}
		}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


@router.post("/google/forecast", tags=["gweather"])
def fetch_google_forecast(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_conditions(coordinates)

		return {"code": 0, "message": "Success", "data": data}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


