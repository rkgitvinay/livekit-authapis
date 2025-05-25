from fastapi import APIRouter
from app.api.models import SuccessResponse

router = APIRouter()

@router.get(
    "/health",
    response_model=SuccessResponse[dict],
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint
    """
    return SuccessResponse.create(
        data={"status": "healthy"},
        message="Service is healthy"
    ) 