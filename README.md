# Urban Flooding Backend API

A FastAPI-based backend service for urban flooding digital twin application. This API provides weather data, forecasts, warnings, and risk assessments to support flood monitoring and prediction systems.

## Features

- **Weather Data**: Current and historical weather information from Bureau of Meteorology (BOM) and google's weather API
- **Forecasts**: Weather forecasting information from Bureau of Meteorology (BOM) and google's weather API
- **Warnings**: Real-time weather warnings and alerts from Bureau of Meteorology (BOM)
- **Risk Assessment**: Flood risk analysis and reporting from Urban Flooding Digital Twin application
- **Health Monitoring**: API health checks and status monitoring
- **User flood report**: Passes user flood reports to and from the digital Twin

## Architecture

```
urban_flooding_backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── data/
│   └── station.json       # Weather station configuration
└── src/
    ├── api/v1/            # API version 1 routes and endpoints
    │   ├── routes.py      # Main API router
    │   └── endpoints/     # Individual endpoint modules
    │       ├── health.py  # Health check endpoints
    │       ├── weather.py # Weather data endpoints (BOM)
    │       ├── forecast.py # Forecast endpoints (BOM)
    │       ├── warnings.py # Warning endpoints (BOM)
    │       ├── gweather.py # Google weather integration (Google)
    │       ├── risk.py    # Risk assessment endpoints (Digital Twin)
    │       └── report.py  # Reporting endpoints (Digital Twin)
    └── core/              # Core functionality
        ├── config.py      # Configuration management
        ├── auth.py        # Authentication
        ├── bom.py         # Bureau of Meteorology integration
        ├── google.py      # Google services integration
        ├── digitaltwin.py # Digital twin functionality
        └── helpers.py     # Utility functions
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd urban_flooding_backend
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a copy of `.example.env` and rename `.env` in the project root.
   Fill in the required variables

### Running the Application

**Development Mode:**

```bash
python main.py
```

**Production Mode:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8118
```

The API will be available at `http://localhost:8118`

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8118/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8118/redoc`
- **OpenAPI JSON Schema**: `http://localhost:8118/openapi.json`

## API Endpoints

### Health Check

- `GET /api/v1/health` - Check API status

### Weather Data

- `POST /api/v1/weather` - Get current weather data
- `POST /api/v1/weather/historical` - Get historical weather data

### Forecasts

- Weather forecast endpoints (see `/docs` for details)

### Warnings

- `POST /api/v1/warnings` - Get location-based weather warnings
- `GET /api/v1/warnings/all` - Get all current weather warnings

### Risk Assessment

- Risk analysis endpoints for flood prediction

### Reports

- Reporting and analytics endpoints

## Authentication

The API uses token-based authentication. Include your API token in the request headers:

```http
Authorization: Bearer your_api_token_here
```

## 🌍 Data Sources

- **Bureau of Meteorology (BOM)**: Australian weather data and warnings
- **Google Weather API**: Additional weather information
- **Digital Twin Platform**: Integration with urban digital twin systems

## Configuration

The application uses environment-based configuration. Key settings include:

- `APP_NAME`: Application name (default: "flood-backend")
- `API_TOKEN`: Authentication token for API access
- `DT_API_TOKEN`: Digital twin platform authentication
- `DT_BASE_URL`: Digital twin platform base URL
- `GOOGLE_API_KEY`: Google API authentication key
- `GOOGLE_BASE_URL`: Google services base URL

## Weather Stations

The application includes predefined weather stations in `data/station.json`, primarily focused on Perth, Australia stations. Each station includes:

- Station name and ID
- Geographic coordinates (latitude/longitude)
- BOM product IDs and URLs
- Historical data access templates

## 🛠️ Development

### Project Structure

The codebase follows a modular architecture:

- **`main.py`**: Application factory and entry point
- **`src/api/v1/`**: API version 1 implementation
- **`src/core/`**: Core business logic and integrations
- **`data/`**: Static data and configuration files

### Dependencies

Key dependencies include:

- **FastAPI**: Modern web framework for APIs
- **Uvicorn**: ASGI server implementation
- **Pydantic**: Data validation and settings management
- **Requests**: HTTP client library
- **Pandas**: Data analysis and manipulation
- **BeautifulSoup4**: HTML/XML parsing
- **Feedparser**: RSS/Atom feed parsing

**Note**: This is a backend API service designed to work with urban flooding digital twin applications. Make sure to configure all required environment variables and API tokens before deployment.
