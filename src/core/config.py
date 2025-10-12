"""
Configuration Management Module

This module handles application configuration using Pydantic settings.
It loads environment variables from a .env file and provides type-safe
access to configuration values throughout the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, ClassVar
import os


class Settings(BaseSettings):
    """
    Application settings configuration.

    This class defines all configuration parameters for the urban flooding
    backend API. Settings are loaded from environment variables and a .env
    file, with type validation provided by Pydantic.

    Attributes:
        APP_NAME (str): Name of the application
        API_TOKEN (Optional[str]): Authentication token for API access
        DT_API_TOKEN (Optional[str]): Digital twin platform authentication token
        DT_BASE_URL (Optional[str]): Base URL for digital twin platform
        GOOGLE_API_KEY (Optional[str]): Google API key for weather services
        GOOGLE_BASE_URL (Optional[str]): Base URL for Google services
        env_path (ClassVar[str]): Path to the .env file
    """

    APP_NAME: str = "flood-backend"
    API_TOKEN: Optional[str] = None
    DT_API_TOKEN: Optional[str] = None
    DT_BASE_URL: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_BASE_URL: Optional[str] = None
    env_path: ClassVar[str] = os.path.join(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    print(f"Loading environment variables from: {env_path}")
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")


# Global settings instance
settings = Settings()
