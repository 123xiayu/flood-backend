import sys
import os
# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from api.v1.routes import api_router
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def create_app() -> FastAPI:
    app = FastAPI(title="flood-backend")
    app.include_router(api_router, prefix="/api/v1")
        
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
