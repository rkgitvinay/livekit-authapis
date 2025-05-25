from fastapi import Request, HTTPException
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
import time
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class APIKeyAuth(APIKeyHeader):
    def __init__(self):
        super().__init__(name=settings.API_KEY_HEADER)

    async def __call__(self, request: Request) -> str:
        api_key = await super().__call__(request)
        if api_key != settings.API_KEY:
            raise HTTPException(
                status_code=403,
                detail="Invalid API key"
            )
        return api_key

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)
        self.limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60  # 1 minute window

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Process request
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {process_time:.2f}s"
        )
        
        return response 