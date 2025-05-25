import uuid
import time
from typing import List, Optional, Dict
from livekit import api
from app.core.config import settings
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class LiveKitServiceError(Exception):
    """Base exception for LiveKit service errors"""
    pass

class LiveKitService:
    """
    Service for interacting with the LiveKit API
    """
    
    @staticmethod
    async def get_rooms() -> List[str]:
        """
        Get a list of all room names from LiveKit
        
        Returns:
            List[str]: List of room names
        """
        try:
            livekit_api = api.LiveKitAPI(url=settings.LIVEKIT_URL)
            rooms_response = await livekit_api.room.list_rooms(api.ListRoomsRequest())
            room_names = [room.name for room in rooms_response.rooms]
            await livekit_api.aclose()
            return room_names
        except Exception as e:
            print(f"Error listing rooms: {e}")
            return []
    
    @staticmethod
    async def generate_room_name() -> str:
        """
        Generate a unique room name
        
        Returns:
            str: A unique room name
        """
        try:
            name = f"room-{str(uuid.uuid4())[:8]}"
            rooms = await LiveKitService.get_rooms()
            while name in rooms:
                name = f"room-{str(uuid.uuid4())[:8]}"
            return name
        except Exception as e:
            logger.error(f"Error generating room name: {str(e)}")
            raise LiveKitServiceError(f"Failed to generate room name: {str(e)}")
    
    @staticmethod
    def generate_token(
        name: str,
        room: str,
        api_key: str,
        api_secret: str,
        metadata: Optional[dict] = None,
        ttl: int = 3600  # 1 hour default
    ) -> Dict:
        """
        Generate a LiveKit access token for a user and room
        
        Args:
            name (str): User's name/identity
            room (str): Room name
            api_key (str): LiveKit API key
            api_secret (str): LiveKit API secret
            metadata (Optional[dict]): Additional metadata for the user
            ttl (int): Token time-to-live in seconds
            
        Returns:
            Dict: Token information including the JWT and expiration
        """
        try:
            # Create a new token
            token = api.AccessToken(api_key, api_secret)
            
            # Set the identity and name
            token = token.with_identity(name).with_name(name)
            
            # Add grants
            token = token.with_grants(api.VideoGrants(
                room_join=True,
                room=room
            ))
            
            # Generate the JWT
            jwt_token = token.to_jwt()
            
            return {
                "token": jwt_token,
                "room": room
            }
        except Exception as e:
            logger.error(f"Error generating token: {str(e)}")
            raise LiveKitServiceError(f"Failed to generate token: {str(e)}")
    
    @staticmethod
    async def delete_room(room_name: str) -> bool:
        """
        Delete a LiveKit room
        
        Args:
            room_name (str): Name of the room to delete
            
        Returns:
            bool: True if room was deleted successfully
        """
        try:
            livekit_api = api.LiveKitAPI(url=settings.LIVEKIT_URL)
            await livekit_api.room.delete_room(api.DeleteRoomRequest(room=room_name))
            await livekit_api.aclose()
            return True
        except Exception as e:
            logger.error(f"Error deleting room {room_name}: {str(e)}")
            raise LiveKitServiceError(f"Failed to delete room: {str(e)}")
