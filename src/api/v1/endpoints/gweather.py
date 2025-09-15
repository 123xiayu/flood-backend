from fastapi import APIRouter
from pydantic import BaseModel
from core.google import fetch_google_conditions, fetch_google_hourly_forecast, fetch_google_daily_forecast

router = APIRouter()

class WeatherRequest(BaseModel):
	lat: float
	lon: float

dev_conditions = {
    "code": 0,
    "message": "Success",
    "data": {
        "weatherConditions": {
            "currentTime": "2025-09-14T13:16:15.266652556Z",
            "timeZone": {
                "id": "Australia/Perth"
            },
            "isDaytime": "false",
            "weatherCondition": {
                "": "https://maps.gstatic.com/weather/v1/mostly_cloudy_night",
                "description": {
                    "text": "Mostly cloudy",
                    "languageCode": "en"
                },
                "type": "MOSTLY_CLOUDY"
            },
            "temperature": {
                "degrees": 12.8,
                "unit": "CELSIUS"
            },
            "feelsLikeTemperature": {
                "degrees": 11,
                "unit": "CELSIUS"
            },
            "dewPoint": {
                "degrees": 5.9,
                "unit": "CELSIUS"
            },
            "heatIndex": {
                "degrees": 12.8,
                "unit": "CELSIUS"
            },
            "windChill": {
                "degrees": 11,
                "unit": "CELSIUS"
            },
            "relativeHumidity": 63,
            "uvIndex": 0,
            "precipitation": {
                "probability": {
                    "percent": 16,
                    "type": "RAIN"
                },
                "snowQpf": {
                    "quantity": 0,
                    "unit": "MILLIMETERS"
                },
                "qpf": {
                    "quantity": 0.0991,
                    "unit": "MILLIMETERS"
                }
            },
            "thunderstormProbability": 10,
            "airPressure": {
                "meanSeaLevelMillibars": 1012.74
            },
            "wind": {
                "direction": {
                    "degrees": 245,
                    "cardinal": "WEST_SOUTHWEST"
                },
                "speed": {
                    "value": 21,
                    "unit": "KILOMETERS_PER_HOUR"
                },
                "gust": {
                    "value": 36,
                    "unit": "KILOMETERS_PER_HOUR"
                }
            },
            "visibility": {
                "distance": 16,
                "unit": "KILOMETERS"
            },
            "cloudCover": 69,
            "currentConditionsHistory": {
                "temperatureChange": {
                    "degrees": -3.6,
                    "unit": "CELSIUS"
                },
                "maxTemperature": {
                    "degrees": 17.6,
                    "unit": "CELSIUS"
                },
                "minTemperature": {
                    "degrees": 13.7,
                    "unit": "CELSIUS"
                },
                "snowQpf": {
                    "quantity": 0,
                    "unit": "MILLIMETERS"
                },
                "qpf": {
                    "quantity": 10.3151,
                    "unit": "MILLIMETERS"
                }
            }
        },
        "conditions": {
            "condition": "Mostly cloudy",
            "temperature": 12.8,
            "feels_like": 11,
            "forecast_icon_uri": "https://maps.gstatic.com/weather/v1/mostly_cloudy_night"
        }
    }
}

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

dev_forecast = {
    "code": 0,
    "message": "Success",
    "data": {
        "forecastHours": [
            {
                "interval": {
                    "startTime": "2025-09-14T08:00:00Z",
                    "endTime": "2025-09-14T09:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 16,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Light rain",
                        "languageCode": "en"
                    },
                    "type": "LIGHT_RAIN"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 14.7
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 9.7
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 14.7
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 35
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.3531
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1008.81
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST",
                        "degrees": 270
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 31
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 64
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 72,
                "uvIndex": 1,
                "thunderstormProbability": 10,
                "cloudCover": 87
            },
            {
                "interval": {
                    "startTime": "2025-09-14T09:00:00Z",
                    "endTime": "2025-09-14T10:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 17,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Light rain",
                        "languageCode": "en"
                    },
                    "type": "LIGHT_RAIN"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 14.8
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 9.6
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 14.8
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 35
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.3556
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1009.31
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST",
                        "degrees": 265
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 29
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 61
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 71,
                "uvIndex": 0,
                "thunderstormProbability": 20,
                "cloudCover": 77
            },
            {
                "interval": {
                    "startTime": "2025-09-14T10:00:00Z",
                    "endTime": "2025-09-14T11:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 18,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15.1
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 7.6
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15.1
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.9
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1009.91
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 255
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 29
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 56
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 61,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 55
            },
            {
                "interval": {
                    "startTime": "2025-09-14T11:00:00Z",
                    "endTime": "2025-09-14T12:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 19,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 14.3
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 7.9
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 14.3
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.8
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 25
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.2007
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1011.1
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 245
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 26
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 47
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 66,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 50
            },
            {
                "interval": {
                    "startTime": "2025-09-14T12:00:00Z",
                    "endTime": "2025-09-14T13:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 20,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 13.8
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.4
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 13.8
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 9.8
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1012.01
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 245
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 23
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 39
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 61,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 63
            },
            {
                "interval": {
                    "startTime": "2025-09-14T13:00:00Z",
                    "endTime": "2025-09-14T14:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 21,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Light rain",
                        "languageCode": "en"
                    },
                    "type": "LIGHT_RAIN"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 13.2
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.1
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 13.2
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 9.4
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1012.61
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 245
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 21
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 35
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 62,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 68
            },
            {
                "interval": {
                    "startTime": "2025-09-14T14:00:00Z",
                    "endTime": "2025-09-14T15:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 22,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Light rain",
                        "languageCode": "en"
                    },
                    "type": "LIGHT_RAIN"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 12.9
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.2
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 12.9
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 9.4
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1013.1
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 250
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 19
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 34
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 64,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 80
            },
            {
                "interval": {
                    "startTime": "2025-09-14T15:00:00Z",
                    "endTime": "2025-09-14T16:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 14,
                    "hours": 23,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Light rain",
                        "languageCode": "en"
                    },
                    "type": "LIGHT_RAIN"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 12.7
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.6
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 12.7
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 9.4
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 25
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.1092
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1013.21
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 250
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 29
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 66,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 78
            },
            {
                "interval": {
                    "startTime": "2025-09-14T16:00:00Z",
                    "endTime": "2025-09-14T17:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Light rain",
                        "languageCode": "en"
                    },
                    "type": "LIGHT_RAIN"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 12.3
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.2
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 12.3
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 11
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 9.1
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 25
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1013.41
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 240
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 29
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 66,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 68
            },
            {
                "interval": {
                    "startTime": "2025-09-14T17:00:00Z",
                    "endTime": "2025-09-14T18:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 1,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.7
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.1
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 11.7
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 8.7
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1013.61
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 245
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 29
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 69,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 60
            },
            {
                "interval": {
                    "startTime": "2025-09-14T18:00:00Z",
                    "endTime": "2025-09-14T19:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 2,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.6
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 9.1
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1013.5
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 245
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 31
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 70,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 55
            },
            {
                "interval": {
                    "startTime": "2025-09-14T19:00:00Z",
                    "endTime": "2025-09-14T20:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 3,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/partly_clear",
                    "description": {
                        "text": "Partly cloudy",
                        "languageCode": "en"
                    },
                    "type": "PARTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 12.1
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.1
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 12.1
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 8.9
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1013.5
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 240
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 29
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 66,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 45
            },
            {
                "interval": {
                    "startTime": "2025-09-14T20:00:00Z",
                    "endTime": "2025-09-14T21:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 4,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/partly_clear",
                    "description": {
                        "text": "Partly cloudy",
                        "languageCode": "en"
                    },
                    "type": "PARTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 5.7
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 8.7
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0533
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1014
                },
                "wind": {
                    "direction": {
                        "cardinal": "WEST_SOUTHWEST",
                        "degrees": 240
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 27
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 66,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 50
            },
            {
                "interval": {
                    "startTime": "2025-09-14T21:00:00Z",
                    "endTime": "2025-09-14T22:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 5,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/partly_clear",
                    "description": {
                        "text": "Partly cloudy",
                        "languageCode": "en"
                    },
                    "type": "PARTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.9
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 5.6
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 11.9
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 8.7
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0051
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1014.4
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 235
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 27
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 65,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 53
            },
            {
                "interval": {
                    "startTime": "2025-09-14T22:00:00Z",
                    "endTime": "2025-09-14T23:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 6,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/partly_clear",
                    "description": {
                        "text": "Partly cloudy",
                        "languageCode": "en"
                    },
                    "type": "PARTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 5.4
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 8.6
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1014.95
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 230
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 19
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 32
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "false",
                "relativeHumidity": 65,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 62
            },
            {
                "interval": {
                    "startTime": "2025-09-14T23:00:00Z",
                    "endTime": "2025-09-15T00:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 7,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.3
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 11.8
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 10
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 8.9
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0533
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1015.71
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 235
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 16
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 26
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 69,
                "uvIndex": 0,
                "thunderstormProbability": 10,
                "cloudCover": 60
            },
            {
                "interval": {
                    "startTime": "2025-09-15T00:00:00Z",
                    "endTime": "2025-09-15T01:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 8,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 13.5
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 7.8
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 13.5
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 12
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.4
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1016.75
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 230
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 16
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 26
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 69,
                "uvIndex": 1,
                "thunderstormProbability": 10,
                "cloudCover": 57
            },
            {
                "interval": {
                    "startTime": "2025-09-15T01:00:00Z",
                    "endTime": "2025-09-15T02:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 9,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 14.6
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.8
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 14.6
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 13
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.3
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 35
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.348
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1017.5
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 225
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 18
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 31
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 60,
                "uvIndex": 2,
                "thunderstormProbability": 10,
                "cloudCover": 57
            },
            {
                "interval": {
                    "startTime": "2025-09-15T02:00:00Z",
                    "endTime": "2025-09-15T03:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 10,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15.2
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 7.6
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15.2
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.9
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1017.91
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 230
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 21
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 35
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 61,
                "uvIndex": 3,
                "thunderstormProbability": 10,
                "cloudCover": 50
            },
            {
                "interval": {
                    "startTime": "2025-09-15T03:00:00Z",
                    "endTime": "2025-09-15T04:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 11,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
                    "description": {
                        "text": "Chance of showers",
                        "languageCode": "en"
                    },
                    "type": "CHANCE_OF_SHOWERS"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15.3
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.9
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15.3
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.7
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 20
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1018.36
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 225
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 23
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 39
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 57,
                "uvIndex": 5,
                "thunderstormProbability": 10,
                "cloudCover": 60
            },
            {
                "interval": {
                    "startTime": "2025-09-15T04:00:00Z",
                    "endTime": "2025-09-15T05:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 12,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/mostly_cloudy",
                    "description": {
                        "text": "Mostly cloudy",
                        "languageCode": "en"
                    },
                    "type": "MOSTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15.2
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.7
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15.2
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.6
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1018.56
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 220
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 23
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 39
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 57,
                "uvIndex": 5,
                "thunderstormProbability": 10,
                "cloudCover": 65
            },
            {
                "interval": {
                    "startTime": "2025-09-15T05:00:00Z",
                    "endTime": "2025-09-15T06:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 13,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/mostly_cloudy",
                    "description": {
                        "text": "Mostly cloudy",
                        "languageCode": "en"
                    },
                    "type": "MOSTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15.6
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.4
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15.6
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.6
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0.0991
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1018.3
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 220
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 23
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 39
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 55,
                "uvIndex": 4,
                "thunderstormProbability": 10,
                "cloudCover": 65
            },
            {
                "interval": {
                    "startTime": "2025-09-15T06:00:00Z",
                    "endTime": "2025-09-15T07:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 14,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/partly_cloudy",
                    "description": {
                        "text": "Partly sunny",
                        "languageCode": "en"
                    },
                    "type": "PARTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15.2
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.3
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15.2
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.4
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1018.35
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 220
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 23
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 37
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 56,
                "uvIndex": 3,
                "thunderstormProbability": 10,
                "cloudCover": 55
            },
            {
                "interval": {
                    "startTime": "2025-09-15T07:00:00Z",
                    "endTime": "2025-09-15T08:00:00Z"
                },
                "displayDateTime": {
                    "year": 2025,
                    "month": 9,
                    "day": 15,
                    "hours": 15,
                    "minutes": 0,
                    "seconds": 0,
                    "nanos": 0,
                    "utcOffset": "28800s"
                },
                "weatherCondition": {
                    "iconBaseUri": "https://maps.gstatic.com/weather/v1/partly_cloudy",
                    "description": {
                        "text": "Partly sunny",
                        "languageCode": "en"
                    },
                    "type": "PARTLY_CLOUDY"
                },
                "temperature": {
                    "unit": "CELSIUS",
                    "degrees": 15
                },
                "feelsLikeTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "dewPoint": {
                    "unit": "CELSIUS",
                    "degrees": 6.2
                },
                "heatIndex": {
                    "unit": "CELSIUS",
                    "degrees": 15
                },
                "windChill": {
                    "unit": "CELSIUS",
                    "degrees": 14
                },
                "wetBulbTemperature": {
                    "unit": "CELSIUS",
                    "degrees": 10.3
                },
                "precipitation": {
                    "probability": {
                        "type": "RAIN",
                        "percent": 15
                    },
                    "snowQpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    },
                    "qpf": {
                        "unit": "MILLIMETERS",
                        "quantity": 0
                    }
                },
                "airPressure": {
                    "meanSeaLevelMillibars": 1018.36
                },
                "wind": {
                    "direction": {
                        "cardinal": "SOUTHWEST",
                        "degrees": 220
                    },
                    "speed": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 21
                    },
                    "gust": {
                        "unit": "KILOMETERS_PER_HOUR",
                        "value": 35
                    }
                },
                "visibility": {
                    "unit": "KILOMETERS",
                    "distance": 16
                },
                "iceThickness": {
                    "unit": "MILLIMETERS",
                    "thickness": 0
                },
                "isDaytime": "true",
                "relativeHumidity": 56,
                "uvIndex": 3,
                "thunderstormProbability": 10,
                "cloudCover": 62
            }
        ],
        "timeZone": {
            "id": "Australia/Perth",
            "version": ""
        },
        "nextPageToken": "ChQKEgkzMzMzM_M_wBHXo3A9CvdcQBAYGBgiCwjf_ZnGBhCKysgGKg9BdXN0cmFsaWEvUGVydGg="
    }
}


@router.post("/google/forecast/hourly", tags=["gweather"])
def get_google_forecast(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_hourly_forecast(coordinates)
		# data = dev_forecast

		return {"code": 0, "message": "Success", "data": data}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


@router.post("/google/forecast/daily", tags=["gweather"])
def get_google_forecast(request: WeatherRequest):
	try:
		coordinates = (request.lat, request.lon)
		data = fetch_google_daily_forecast(coordinates)
		# data = dev_forecast

		return {"code": 0, "message": "Success", "data": data}
	except Exception as e:
		return {"code": 1, "message": f"Error: {str(e)}", "data": None}


