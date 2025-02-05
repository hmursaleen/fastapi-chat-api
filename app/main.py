from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from app.websocket import connection_manager as ws_conn, handle_message
from app.auth import create_access_token, verify_token
from app.models import User, Message
from app.config import messages_collection
from typing import List

app = FastAPI()

# Fake user database (Replace with real DB in production)
fake_users_db = {
    "alice": {"username": "alice", "password": "hashedpassword1"},
    "bob": {"username": "bob", "password": "hashedpassword2"},
}


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chat API"}


@app.post("/token")
#Authenticates users and returns a JWT token.
async def login(user: User):
    if user.username in fake_users_db and user.password == fake_users_db[user.username]["password"]:
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}



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
            await handle_message(room, username, data)  # Save message & broadcast
            #Calls handle_message() to store messages in MongoDB before broadcasting.

    except WebSocketDisconnect:
        ws_conn.disconnect(room, username)
        await ws_conn.broadcast(room, f"[{room}] {username} has left the chat.")



#Retrieves past messages for a given chat room. Defaults to last 50 messages, but can increase if needed.
@app.get("/messages/{room}", response_model=List[Message])
async def get_chat_history(room: str, limit: int = Query(50, description="Number of messages to fetch")):
    messages = await messages_collection.find({"room": room}).sort("timestamp", -1).limit(limit).to_list(length=limit)
    return messages
