from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import settings
from app.core.middleware import RateLimitMiddleware, LoggingMiddleware
from app.core.logging import setup_logging
import logging
import sys

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    application = FastAPI(
        title="LiveKit Auth APIs",
        description="Authentication and room management APIs for LiveKit",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add rate limiting middleware
    application.add_middleware(RateLimitMiddleware)
    
    # Add logging middleware
    application.add_middleware(LoggingMiddleware)
    
    # Include API routes
    application.include_router(router)
    
    @application.on_event("startup")
    async def startup_event():
        logger.info("Starting up LiveKit Auth APIs")
        logger.debug(f"Environment: {settings.ENVIRONMENT}")
        logger.debug(f"LiveKit URL: {settings.LIVEKIT_URL}")
    
    @application.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down LiveKit Auth APIs")
    
    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
