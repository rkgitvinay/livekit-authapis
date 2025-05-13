from fastapi import APIRouter, Depends, Query
from app.services.livekit_service import LiveKitService
from app.core.config import settings

router = APIRouter()

@router.get("/getToken")
async def get_token(
    name: str = Query("my name", description="User's name/identity"),
    room: str = Query(None, description="Room name (optional, will be generated if not provided)")
):
    """
    Generate a LiveKit access token for a user and room
    
    Args:
        name: User's name/identity
        room: Room name (optional, will be generated if not provided)
        
    Returns:
        str: JWT token for LiveKit access
    """
    if not room:
        room = await LiveKitService.generate_room_name()
    
    token = LiveKitService.generate_token(
        name=name,
        room=room,
        api_key=settings.LIVEKIT_API_KEY,
        api_secret=settings.LIVEKIT_API_SECRET
    )
    
    return token
