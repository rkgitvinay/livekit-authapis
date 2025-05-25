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
    async def get_rooms() -> List[Dict]:
        """
        Get a list of all room names from LiveKit
        
        Returns:
            List[Dict]: List of room data including name, creation time, and empty timeout
        """
        try:
            logger.debug(f"Connecting to LiveKit at {settings.LIVEKIT_URL}")
            livekit_api = api.LiveKitAPI(
                url=settings.LIVEKIT_URL,
                api_key=settings.LIVEKIT_API_KEY,
                api_secret=settings.LIVEKIT_API_SECRET
            )
            
            logger.debug("Requesting room list from LiveKit")
            rooms_response = await livekit_api.room.list_rooms(api.ListRoomsRequest())
            
            if not hasattr(rooms_response, 'rooms'):
                logger.error("Invalid response from LiveKit: missing 'rooms' attribute")
                raise LiveKitServiceError("Invalid response from LiveKit server")
            
            rooms_data = []
            for room in rooms_response.rooms:
                created_at = room.creation_time
                if hasattr(created_at, 'timestamp'):
                    created_at = int(created_at.timestamp())
                
                rooms_data.append({
                    "name": room.name,
                    "created_at": created_at,
                    "empty_timeout": room.empty_timeout
                })
            
            logger.debug(f"Found {len(rooms_data)} rooms")
            await livekit_api.aclose()
            return rooms_data
            
        except api.ApiException as e:
            logger.error(f"LiveKit API error: {str(e)}")
            raise LiveKitServiceError(f"LiveKit API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error listing rooms: {str(e)}")
            raise LiveKitServiceError(f"Failed to list rooms: {str(e)}")
    
    @staticmethod
    async def create_room(room_name: str, empty_timeout: int = 300) -> Dict:
        """
        Create a new LiveKit room
        
        Args:
            room_name (str): Name of the room to create
            empty_timeout (int): Time in seconds to wait before deleting empty room
            
        Returns:
            Dict: Room information including name and creation time
        """
        try:
            logger.debug(f"Creating room {room_name} with timeout {empty_timeout}")
            logger.debug(f"Using LiveKit URL: {settings.LIVEKIT_URL}")
            livekit_api = api.LiveKitAPI(
                url=settings.LIVEKIT_URL,
                api_key=settings.LIVEKIT_API_KEY,
                api_secret=settings.LIVEKIT_API_SECRET
            )
            create_request = api.CreateRoomRequest(
                name=room_name,
                empty_timeout=empty_timeout
            )
            room = await livekit_api.room.create_room(create_request)
            await livekit_api.aclose()
            
            # Handle creation_time which could be either int or datetime
            created_at = room.creation_time
            if hasattr(created_at, 'timestamp'):
                created_at = int(created_at.timestamp())
            
            return {
                "name": room.name,
                "created_at": created_at,
                "empty_timeout": room.empty_timeout
            }
        except Exception as e:
            logger.error(f"Error creating room {room_name}: {str(e)}")
            raise LiveKitServiceError(f"Failed to create room: {str(e)}")
    
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
            livekit_api = api.LiveKitAPI(
                url=settings.LIVEKIT_URL,
                api_key=settings.LIVEKIT_API_KEY,
                api_secret=settings.LIVEKIT_API_SECRET
            )
            await livekit_api.room.delete_room(api.DeleteRoomRequest(room=room_name))
            await livekit_api.aclose()
            return True
        except Exception as e:
            logger.error(f"Error deleting room {room_name}: {str(e)}")
            raise LiveKitServiceError(f"Failed to delete room: {str(e)}")
