from fastapi import WebSocket, WebSocketDisconnect, Depends
from app.auth import verify_token
from typing import List, Dict
from app.redis_pubsub import redis_pubsub
import asyncio
from app.config import messages_collection
from app.models import Message
from datetime import datetime


#Stores a chat message in MongoDB    
async def save_message(room: str, sender: str, content: str):
    message_data = Message(
        room=room,
        sender=sender,
        content=content,
        timestamp=datetime.utcnow(),
    ).dict()
    await messages_collection.insert_one(message_data)


#Handles incoming messages: stores them and broadcasts to WebSocket clients.
async def handle_message(room: str, sender: str, content: str):
    await save_message(room, sender, content)  # Save to MongoDB
    await connection_manager.broadcast(room, f"[{room}] {sender}: {content}")  # Send to WebSockets


'''
The following class:
    Each room gets its own list of connected clients.
    Clients only receive messages from their room.
    Uses background tasks (asyncio.create_task) to listen for room messages
'''
class ConnectionManager:
    
    def __init__(self):
        self.active_rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket, username: str):
        await websocket.accept() #Accept WebSocket connection and authenticate user.
        if room not in self.active_rooms:
            self.active_rooms[room] = {}
        self.active_rooms[room][username] = websocket
        asyncio.create_task(self.listen_redis(room))  # Start listening for room messages

    def disconnect(self, room: str, username: str):
        if room in self.active_rooms and username in self.active_rooms[room]:
            del self.active_rooms[room][username] #Remove user from chat room when disconnected.
        if not self.active_rooms[room]:  # If no users left, delete room
            del self.active_rooms[room]

    async def broadcast(self, room: str, message: str):
        redis_pubsub.publish(room, message)  #Sends a message to all WebSocket clients in a specific room.

    async def listen_redis(self, room: str):
        async for message in redis_pubsub.subscribe(room): #Listens to Redis and forwards messages to WebSocket clients.
            for user, connection in self.active_rooms.get(room, {}).items():
                await connection.send_text(message)


connection_manager = ConnectionManager() #create instance of the class