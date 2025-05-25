from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.user import router as user_router
from app.api.routes.agent import router as agent_router

# Create main router
router = APIRouter()

# Include all route modules
router.include_router(health_router, tags=["Health"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(agent_router, prefix="/agent", tags=["Agent"]) 