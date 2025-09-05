
from fastapi import APIRouter
from pydantic import BaseModel
from core.bom import fetch_weather_observation
from core.bom import parse_forecast_for_station
from core.bom import fetch_bom_forecast_xml
from core.helpers import find_nearest_station

router = APIRouter()

class WeatherRequest(BaseModel):
	lat: float
	lon: float

@router.post("/forecast", tags=["forecast"])
def get_forecast(request: WeatherRequest):
	try:
		nearest_station = find_nearest_station(request.lat, request.lon)
		if not nearest_station:
			return {"code": 1, "message": "No weather station found", "data": None}
		xml_content = fetch_bom_forecast_xml()
		forecasts = parse_forecast_for_station(xml_content, nearest_station['AAC'])
		return {"code": 0, "message": "Success", "data": forecasts}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}

# New endpoint: /weathercondition
@router.post("/weathercondition", tags=["weather"])
def get_weather_condition(request: WeatherRequest):
	try:
		nearest_station = find_nearest_station(request.lat, request.lon)
		if not nearest_station:
			return {"code": 1, "message": "No weather station found", "data": None}
		# Get first precis and element (icon code) from forecast
		xml_content = fetch_bom_forecast_xml()
		forecasts = parse_forecast_for_station(xml_content, nearest_station['AAC'])
		precis = None
		forecast_icon_code = None
		if forecasts:
			precis = forecasts[0]['forecast'].get('precis')
			# Find the first 'element' tag value in the first forecast period
			# The 'element' tag is usually used for icon codes in BOM XML
			forecast_icon_code = forecasts[0]['forecast'].get('element')
		# Get temperature from weather observation
		observations = fetch_weather_observation(nearest_station)
		temperature = None
		if observations:
			temperature = observations[0].get('air_temp')
		return {
			"code": 0,
			"message": "Success",
			"data": {
				"precis": precis,
				"temperature": temperature,
				"forecast_icon_code": forecast_icon_code
			}
		}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}
