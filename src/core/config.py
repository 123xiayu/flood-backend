from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "flood-backend"
    ENV: str = "dev"
    API_TOKEN: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
