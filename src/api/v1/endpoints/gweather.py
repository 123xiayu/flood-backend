from fastapi import APIRouter
from pydantic import BaseModel
from core.google import fetch_google_conditions, fetch_google_hourly_forecast, fetch_google_daily_forecast, fetch_google_history

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

		return {"code": 0, "message": "Success", "data": {
			"weatherConditions":	data,
		  	"conditions":	{
				"condition": condition,
				"temperature": temp,
				"feels_like": feels_like,
				"forecast_icon_uri": forecast_icon_uri
				}
			}
		}
		# return dev_conditions
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


@router.post("/google/forecast/hourly", tags=["gweather"])
def get_google_forecast_hourly(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_hourly_forecast(coordinates)

		return {"code": 0, "message": "Success", "data": data}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


@router.post("/google/forecast/daily", tags=["gweather"])
def get_google_forecast_daily(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_daily_forecast(coordinates)

		return {"code": 0, "message": "Success", "data": data}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


@router.post("/google/history", tags=["gweather"])
def get_google_history(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_history(coordinates)

		return {"code": 0, "message": "Success", "data": data}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}



