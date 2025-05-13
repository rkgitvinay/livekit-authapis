import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application settings loaded from environment variables
    """
    def __init__(self):
        self.LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
        self.LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
        self.LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")
        
        # Parse ALLOWED_ORIGINS
        origins_str = os.getenv("ALLOWED_ORIGINS", "")
        if origins_str:
            self.ALLOWED_ORIGINS = [origin.strip() for origin in origins_str.split(",") if origin.strip()]
        else:
            self.ALLOWED_ORIGINS = ["*"]  # Default to allow all origins
        
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "5001"))
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
