import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # LiveKit Configuration
    LIVEKIT_URL: str
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LiveKit Auth API"
    
    # Security
    ALLOWED_ORIGINS: List[str] = ["*"]
    API_KEY_HEADER: str = "X-API-Key"
    API_KEY: str = "6d3c934fc96e5d669f28f209e06e5e2f"  # For API authentication
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 5001
    DEBUG: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
