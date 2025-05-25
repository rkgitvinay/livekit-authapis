# LiveKit Authentication APIs

A FastAPI-based service for managing LiveKit authentication and room management. This service provides APIs for generating LiveKit tokens, managing rooms, and handling user authentication.

## Features

- LiveKit token generation with customizable metadata
- Room management (list, create, delete)
- User authentication and management
- API key-based authentication
- Standardized response format
- Comprehensive error handling
- Rate limiting
- Request validation
- Detailed API documentation

## Project Structure

```
livekit-authapis/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py      # Main router configuration
│   │   │   ├── health.py        # Health check endpoints
│   │   │   ├── user.py          # User management endpoints
│   │   │   └── agent.py         # LiveKit agent and room management
│   │   └── models.py            # Request/Response models
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   ├── middleware.py        # Custom middleware
│   │   └── logging.py           # Logging configuration
│   └── services/
│       └── livekit_service.py   # LiveKit service implementation
├── tests/                       # Test files
├── .env.example                 # Example environment variables
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## API Endpoints

### Health Check
- `GET /health` - Check service health status

### User Management (`/user`)
- `GET /` - Get current user information
- `POST /register` - Register a new user
- `PUT /profile` - Update user profile

### LiveKit Agent (`/agent`)
- `POST /token` - Generate LiveKit access token
- `GET /rooms` - List all active LiveKit rooms
- `DELETE /rooms/{room_name}` - Delete a specific LiveKit room

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd livekit-authapis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration:
```env
# LiveKit Configuration
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_HOST=your_livekit_host

# API Configuration
API_KEY=your_api_key
ENVIRONMENT=development
LOG_LEVEL=INFO
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Response Format

All API responses follow a standardized format:

### Success Response
```json
{
    "status": "success",
    "message": "Operation successful",
    "data": {
        // Response data specific to the endpoint
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error message",
    "code": "ERROR_CODE",
    "details": {
        // Additional error details (optional)
    }
}
```

## Authentication

All endpoints (except health check) require API key authentication. Include the API key in the request header:

```
X-API-Key: your_api_key
```

## Error Codes

- `TOKEN_GENERATION_ERROR` - Error generating LiveKit token
- `ROOM_LIST_ERROR` - Error listing LiveKit rooms
- `ROOM_DELETION_ERROR` - Error deleting LiveKit room
- `INTERNAL_ERROR` - Unexpected server error

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project follows PEP 8 guidelines. Use `black` for code formatting:
```bash
black .
```

## License

[Your License]

## Contributing

[Your Contributing Guidelines] 
