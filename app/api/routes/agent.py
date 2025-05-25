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
    ErrorResponse,
    RoomData
)
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
api_key_auth = APIKeyAuth()

class CreateRoomRequest(BaseModel):
    name: str
    empty_timeout: int = 300

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

        if not request.name:
            request.name = await LiveKitService.generate_user_name()
        
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

@router.get("/rooms", response_model=SuccessResponse[RoomListData])
async def list_rooms(
    auth: APIKeyAuth = Depends(api_key_auth)
) -> SuccessResponse[RoomListData]:
    """
    List all active LiveKit rooms
    """
    try:
        rooms_data = await LiveKitService.get_rooms()
        return SuccessResponse(
            status="success",
            message="Rooms retrieved successfully",
            data=RoomListData(rooms=rooms_data)
        )
    except LiveKitServiceError as e:
        logger.error(f"LiveKit service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                status="error",
                message=str(e),
                code="LIVEKIT_ERROR",
                details=None
            ).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error listing rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                status="error",
                message="Failed to list rooms",
                code="INTERNAL_ERROR",
                details=str(e)
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

@router.post(
    "/rooms",
    response_model=SuccessResponse[RoomData],
    responses={
        400: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def create_room(
    request: CreateRoomRequest,
    api_key: str = Depends(api_key_auth)
):
    """
    Create a new LiveKit room
    
    Args:
        request: Room creation request containing name and optional empty timeout
        api_key: API key for authentication
        
    Returns:
        SuccessResponse[RoomData]: Created room information
    """
    try:
        room_info = await LiveKitService.create_room(
            room_name=request.name,
            empty_timeout=request.empty_timeout
        )
        print(room_info)
        return SuccessResponse.create(
            data=RoomData(**room_info),
            message="Room created successfully"
        )
    except LiveKitServiceError as e:
        logger.error(f"Error creating room: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create(
                message=str(e),
                code="ROOM_CREATION_ERROR"
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