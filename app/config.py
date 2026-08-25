import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


from pydantic import ConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "RailHelpAI"
    ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"
    
    # SQLite Database URL
    DATABASE_URL: str = "sqlite:///./railhelpai.db"
    
    # Frontend URL configuration
    BACKEND_API_URL: str = "http://127.0.0.1:8000/api/v1"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



settings = Settings()
