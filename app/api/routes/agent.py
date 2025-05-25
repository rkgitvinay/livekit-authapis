from fastapi import APIRouter, Depends, HTTPException, status
from app.services.livekit_service import LiveKitService, LiveKitServiceError
from app.core.config import settings
from app.core.middleware import APIKeyAuth
from app.api.models import (
    TokenRequest,
    TokenData,
    RoomListData,
    MessageData,
    SuccessResponse,
    ErrorResponse
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
api_key_auth = APIKeyAuth()

@router.post(
    "/token",
    response_model=SuccessResponse[TokenData],
    responses={
        400: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_token(
    request: TokenRequest,
    api_key: str = Depends(api_key_auth)
):
    """
    Generate a LiveKit access token for a user and room
    
    Args:
        request: Token request containing user name and optional room name
        api_key: API key for authentication
        
    Returns:
        SuccessResponse[TokenData]: Token information including JWT and room details
    """
    try:
        if not request.room:
            request.room = await LiveKitService.generate_room_name()
        
        token_info = LiveKitService.generate_token(
            name=request.name,
            room=request.room,
            api_key=settings.LIVEKIT_API_KEY,
            api_secret=settings.LIVEKIT_API_SECRET,
            metadata=request.metadata
        )
        
        return SuccessResponse.create(
            data=TokenData(**token_info),
            message="Token generated successfully"
        )
    except LiveKitServiceError as e:
        logger.error(f"Error generating token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message=str(e),
                code="TOKEN_GENERATION_ERROR"
            ).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message="Internal server error",
                code="INTERNAL_ERROR"
            ).dict()
        )

@router.get(
    "/rooms",
    response_model=SuccessResponse[RoomListData],
    responses={
        403: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def list_rooms(api_key: str = Depends(api_key_auth)):
    """
    Get a list of all active LiveKit rooms
    
    Args:
        api_key: API key for authentication
        
    Returns:
        SuccessResponse[RoomListData]: List of active rooms with their details
    """
    try:
        rooms = await LiveKitService.get_rooms()
        return SuccessResponse.create(
            data=RoomListData(rooms=rooms),
            message="Rooms retrieved successfully"
        )
    except LiveKitServiceError as e:
        logger.error(f"Error listing rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message=str(e),
                code="ROOM_LIST_ERROR"
            ).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message="Internal server error",
                code="INTERNAL_ERROR"
            ).dict()
        )

@router.delete(
    "/rooms/{room_name}",
    response_model=SuccessResponse[MessageData],
    responses={
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def delete_room(room_name: str, api_key: str = Depends(api_key_auth)):
    """
    Delete a LiveKit room
    
    Args:
        room_name: Name of the room to delete
        api_key: API key for authentication
        
    Returns:
        SuccessResponse[MessageData]: Success message
    """
    try:
        await LiveKitService.delete_room(room_name)
        return SuccessResponse.create(
            data=MessageData(message=f"Room {room_name} deleted successfully"),
            message="Room deleted successfully"
        )
    except LiveKitServiceError as e:
        logger.error(f"Error deleting room: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message=str(e),
                code="ROOM_DELETION_ERROR"
            ).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message="Internal server error",
                code="INTERNAL_ERROR"
            ).dict()
        ) 