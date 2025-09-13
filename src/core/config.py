from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, ClassVar
import os



class Settings(BaseSettings):
    APP_NAME: str = "flood-backend"
    ENV: str = "dev"
    API_TOKEN: Optional[str] = None
    api_key: str = ""  # Add this line for API key from .env
    # Use absolute path for .env file for cross-platform compatibility
    env_path: ClassVar[str] = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

settings = Settings()
