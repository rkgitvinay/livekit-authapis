from pydantic import BaseModel, Field
from typing import Optional, List, TypeVar, Generic, Any

T = TypeVar('T')

class BaseResponse(BaseModel):
    """Base response model with status and message"""
    status: str = Field(..., description="Response status (success/error)")
    message: str = Field(..., description="Response message")

class SuccessResponse(BaseResponse, Generic[T]):
    """Standard success response model"""
    data: T = Field(..., description="Response data")
    
    @classmethod
    def create(cls, data: T, message: str = "Operation successful") -> "SuccessResponse[T]":
        return cls(status="success", message=message, data=data)

class ErrorResponse(BaseResponse):
    """Standard error response model"""
    code: str = Field(..., description="Error code")
    details: Optional[dict] = Field(None, description="Additional error details")
    
    @classmethod
    def create(cls, message: str, code: str, details: Optional[dict] = None) -> "ErrorResponse":
        return cls(status="error", message=message, code=code, details=details)

# Request Models
class TokenRequest(BaseModel):
    name: Optional[str] = Field(..., description="User's name/identity")
    room: Optional[str] = Field(None, description="Room name (optional, will be generated if not provided)")
    metadata: Optional[dict] = Field(None, description="Additional metadata for the user")

# Response Data Models
class TokenData(BaseModel):
    token: str = Field(..., description="JWT token for LiveKit access")
    room: str = Field(..., description="Room name")

class RoomInfo(BaseModel):
    name: str = Field(..., description="Room name")
    num_participants: int = Field(..., description="Number of participants in the room")
    created_at: int = Field(..., description="Room creation timestamp")

class RoomListData(BaseModel):
    rooms: List[RoomInfo] = Field(..., description="List of active rooms")

class MessageData(BaseModel):
    message: str = Field(..., description="Operation result message") 