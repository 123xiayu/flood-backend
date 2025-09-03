from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "flood-backend"
    ENV: str = "dev"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
