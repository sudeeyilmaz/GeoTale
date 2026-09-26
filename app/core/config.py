from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "GeoTale"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://geotale_user:geotale_password@localhost:5432/geotale_db"
    
    # JWT Auth
    SECRET_KEY: str = "geotale_super_secret_jwt_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 gün

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
