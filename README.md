# LiveKit Auth API

A FastAPI application for LiveKit room management and token generation.

## Features

- Generate LiveKit access tokens for users
- Automatic room creation and management
- Configurable CORS settings via environment variables
- Modern FastAPI framework with async support

## Project Structure

```
livekit-auth-api/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── livekit_service.py
│   ├── __init__.py
│   └── main.py
├── .env
├── main.py
├── README.md
└── requirements.txt
```

## Setup

1. Clone the repository
2. Set up your environment variables in `.env` file:
   ```
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   HOST=0.0.0.0
   PORT=5001
   DEBUG=True
   ```
3. Install dependencies using uv:
   ```
   uv pip install -r requirements.txt
   ```

## Running the Application

```
python main.py
```

Or using uvicorn directly:

```
uvicorn app.main:app --host 0.0.0.0 --port 5001 --reload
```

## API Endpoints

### GET /getToken

Generate a LiveKit access token for a user and room.

**Query Parameters:**
- `name` (optional): User's name/identity (default: "my name")
- `room` (optional): Room name (if not provided, a unique room name will be generated)

**Response:**
- A JWT token string for LiveKit access

## Development

This project uses uv for package management. To add new dependencies:

```
uv pip install package_name
```

Then update the requirements.txt file:

```
uv pip freeze > requirements.txt
```
"# livekit-authapis" 
