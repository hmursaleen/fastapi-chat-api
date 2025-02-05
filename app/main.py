from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.websocket import connection_manager as ws_conn #the instance of ConnectionManager class
from app.auth import create_access_token, verify_token
from app.models import User


app = FastAPI()

# Fake user database (Replace with real DB in production)
fake_users_db = {
    "alice": {"username": "alice", "password": "hashedpassword1"},
    "bob": {"username": "bob", "password": "hashedpassword2"},
}


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chat API"}


'''
The following function:
    Each WebSocket connection must specify a room in the URL.
    Users only receive messages from their room.
'''


@app.post("/token")
async def login(user: User):
    """Authenticates users and returns a JWT token."""
    if user.username in fake_users_db and user.password == fake_users_db[user.username]["password"]:
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}


#message showing twice to each user

@app.websocket("/ws/{room}")
#Handles WebSocket connections with JWT authentication.
async def websocket_endpoint(room: str, websocket: WebSocket):
    token = websocket.query_params.get("token") # Extract token from query parameters
    if not token:
        await websocket.close(code=1008)  # Policy Violation
        return
    
    try:
        username = verify_token(token)  # Validate token and get username
    except HTTPException:
        await websocket.close(code=1008)  # Unauthorized
        return

    await ws_conn.connect(room, websocket, username)

    try:
        while True:
            data = await websocket.receive_text()
            await ws_conn.broadcast(room, f"[{room}] {username}: {data}")
    except WebSocketDisconnect:
        ws_conn.disconnect(room, username)
        await ws_conn.broadcast(room, f"[{room}] {username} has left the chat.")
