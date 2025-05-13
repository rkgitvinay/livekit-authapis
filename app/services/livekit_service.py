import uuid
from typing import List
from livekit import api
from app.core.config import settings

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
        name = f"room-{str(uuid.uuid4())[:8]}"
        rooms = await LiveKitService.get_rooms()
        while name in rooms:
            name = f"room-{str(uuid.uuid4())[:8]}"
        return name
    
    @staticmethod
    def generate_token(name: str, room: str, api_key: str, api_secret: str) -> str:
        """
        Generate a LiveKit access token for a user and room
        
        Args:
            name (str): User's name/identity
            room (str): Room name
            api_key (str): LiveKit API key
            api_secret (str): LiveKit API secret
            
        Returns:
            str: JWT token for LiveKit access
        """
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
        return token.to_jwt()
