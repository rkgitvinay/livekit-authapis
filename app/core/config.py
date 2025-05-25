import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache
import json

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # LiveKit Configuration (Required)
    LIVEKIT_API_KEY: str = ""  # Required: Your LiveKit API key
    LIVEKIT_API_SECRET: str = ""  # Required: Your LiveKit API secret
    LIVEKIT_URL: str = "http://localhost:7880"  # Optional: LiveKit server URL
    LIVEKIT_HOST: str = "http://localhost:7880"  # Optional: LiveKit host URL
    
    # API Configuration (Required)
    API_KEY: str = ""  # Required: Your API key for authentication
    API_KEY_HEADER: str = "X-API-Key"  # Header name for API key authentication
    API_V1_STR: str = "/v1"
    
    # Optional Configuration
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    DEBUG: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name == "ALLOWED_ORIGINS":
                return json.loads(raw_val)
            return raw_val

    def validate_settings(self):
        """Validate required settings"""
        if not self.LIVEKIT_API_KEY:
            raise ValueError("LIVEKIT_API_KEY is required")
        if not self.LIVEKIT_API_SECRET:
            raise ValueError("LIVEKIT_API_SECRET is required")
        if not self.API_KEY:
            raise ValueError("API_KEY is required")

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_settings()
    return settings

settings = get_settings()
