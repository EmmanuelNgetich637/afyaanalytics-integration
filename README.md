# AfyaAnalytics Integration Platform

A full-stack integration system that demonstrates a secure, real-time handshake authentication flow with AfyaAnalytics APIs, built using Flask (backend) and a modular JavaScript frontend.

## Overview

This project simulates a real-world third-party API integration using a structured authentication lifecycle:

1. Create session  
2. Initiate handshake  
3. Complete handshake  
4. Receive and manage tokens  
5. Track expiry and auto-refresh tokens  

It follows a production-style architecture with session isolation, token lifecycle management, real-time UI feedback, and backend-synced state.

## Key Features

### Authentication and Sessions
- Session-based authentication flow
- Two-step handshake system (initiate and complete)
- Secure token exchange (access and refresh tokens)

### Token Lifecycle Management
- Backend-synced expiry using `expires_in_seconds`
- Separate timers for:
  - Handshake token (15 minutes)
  - Access token (6 hours)
- Real-time countdown UI
- Expiry detection and UI state updates

### Auto Token Refresh
- Automatic refresh before token expiry
- Seamless session continuity
- No manual re-authentication required

### Observability and Debugging
- API request and response logs panel
- Step-by-step flow tracking
- Real-time system feedback

### Frontend Experience
- Clean dashboard interface
- Step-based flow visualization
- Token display with copy functionality
- Live status indicators

### Backend Architecture
- Flask REST API
- Session-based state management
- Token handling utilities
- External API service abstraction

## Project Structure

afyaanalytics-integration/

backend/
- app.py  
- config.py  
- services/  
  - afya_service.py  
- utils/  
  - token_manager.py  
  - logger.py  
- sessions/  
  - session_store.py  
- requirements.txt  

frontend/
- index.html  
- css/  
  - styles.css  
- js/  
  - app.js  
  - api.js  
  - timer.js  

screenshots/  
run.sh  
README.md  

## Installation and Setup

### Clone Repository

git clone https://github.com/EmmanuelNgetich637/afyaanalytics-integration.git

cd afyaanalytics-integration


### Setup Backend

cd backend
python -m venv venv
source venv/bin/activate

venv\Scripts\activate (Windows)

pip install -r requirements.txt


### Run Server

python app.py


Server runs on:

http://127.0.0.1:5000


### Open Frontend

Open:

frontend/index.html

in your browser.

## API Flow

### Create Session

POST /session/create


Response:

{
"success": true,
"session_id": "uuid"
}


### Initiate Handshake

POST /session/<session_id>/initiate


Response:

{
"success": true,
"data": {
"handshake_token": "...",
"expires_in_seconds": 900
}
}


### Complete Handshake

POST /session/<session_id>/complete


Response:

{
"success": true,
"data": {
"access_token": "...",
"refresh_token": "...",
"expires_at": "...",
"expires_in_seconds": 21600
}
}


### Refresh Token

POST /refresh-token


### Get Session Data

GET /session/<session_id>


## Testing with curl


curl -X POST http://127.0.0.1:5000/session/create

curl -X POST http://127.0.0.1:5000/session/
<SESSION_ID>/initiate

curl -X POST http://127.0.0.1:5000/session/
<SESSION_ID>/complete

curl -X POST http://127.0.0.1:5000/refresh-token

-H "Content-Type: application/json"
-d '{"refresh_token":"YOUR_TOKEN"}'


## Architecture Overview

SESSION  
↓  
HANDSHAKE (15 minute token)  
↓  
AUTHENTICATED  
↓  
ACCESS TOKEN (6 hour lifecycle)  
↓  
AUTO REFRESH  

## Frontend Features

- Start handshake action  
- Complete handshake action  
- Handshake and access token display  
- Dual expiry countdown timers  
- Auto-refresh handling  
- Logs panel  
- Copy-to-clipboard functionality  

## Security Notes

- Tokens stored in memory (development only)
- No persistent database
- CORS enabled for local use
- Do not expose real credentials in production

## Future Improvements

- Session persistence across reloads  
- Database integration (PostgreSQL or Redis)  
- WebSocket-based live updates  
- Retry and exponential backoff system  
- Environment-based secrets management  
- Automated testing  
- Docker containerization  

## Author

Emmanuel Ng'etich

GitHub: https://github.com/EmmanuelNgetich637

## License

MIT License