from fastapi import APIRouter
import requests
import xml.etree.ElementTree as ET
from pydantic import BaseModel

from core.helpers import find_nearest_station

router = APIRouter()

class WeatherRequest(BaseModel):
    lat: float
    lon: float

@router.post("/forecast", tags=["forecast"])
def get_forecast(request: WeatherRequest):

	# Find nearest station
	nearest_station = find_nearest_station(request.lat, request.lon)
	print(nearest_station['AAC'])
	
	url = "http://www.bom.gov.au/fwo/IDW14199.xml"

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Encoding': 'gzip, deflate'
	}

	try:

		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			return {
				"code": 1,
				"message": f"Failed to fetch forecast data: HTTP {response.status_code}",
				"data": None
			}
		
		# Parse XML
		root = ET.fromstring(response.content)
		forecasts = []

		# Extract forecast periods and text
		for area in root.findall(".//area"):
			if area.attrib.get("aac", "") != nearest_station['AAC']:
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
						period_data["forecast"][elem.attrib.get("type", "text")] = elem.text
					else:
						period_data["forecast"][elem.tag] = elem.text
				forecasts.append(period_data)
		return {
			"code": 0,
			"message": "Success",
			"data": forecasts
		}
	
	except Exception as e:
		return {
			"code": 1,
			"message": f"Error: {str(e)}",
			"data": None
		}
