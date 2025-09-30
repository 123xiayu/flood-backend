from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, ClassVar
import os


class Settings(BaseSettings):
    APP_NAME: str = "flood-backend"
    API_TOKEN: Optional[str] = None
    DT_API_TOKEN: Optional[str] = None
    DT_BASE_URL: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_BASE_URI: Optional[str] = None
    env_path: ClassVar[str] = os.path.join(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")


settings = Settings()
