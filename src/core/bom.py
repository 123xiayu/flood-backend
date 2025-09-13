import xml.etree.ElementTree as ET
import requests


def fetch_weather_observation(station):
	# todo: add user-agent header to avoid 403 from bom.gov.au
	# todo: add error handling for non-200 responses
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}
	response = requests.get(station['url'], headers=headers)
	if response.status_code != 200:
		raise Exception(f"Failed to fetch weather data: HTTP {response.status_code}")
	weather_data = response.json()
	if 'observations' not in weather_data or 'data' not in weather_data['observations']:
		raise Exception("Invalid weather data format")
	observations = weather_data['observations']['data']
	return observations


def parse_forecast_for_station(xml_content, aac):
	root = ET.fromstring(xml_content)
	forecasts = []
	for area in root.findall(".//area"):
		if area.attrib.get("aac", "") != aac:
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
	return forecasts


def fetch_bom_forecast_xml():
	url = "http://www.bom.gov.au/fwo/IDW14199.xml"
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Encoding': 'gzip, deflate'
	}
	response = requests.get(url, headers=headers)
	if response.status_code != 200:
		raise Exception(f"Failed to fetch forecast data: HTTP {response.status_code}")
	return response.content