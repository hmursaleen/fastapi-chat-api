from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
from app.redis_pubsub import redis_pubsub
import asyncio

'''
The following class:
    Each room gets its own list of connected clients.
    Clients only receive messages from their room.
    Uses background tasks (asyncio.create_task) to listen for room messages
'''
class ConnectionManager:
    
    def __init__(self):
        self.active_rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept() #Accepts a WebSocket connection and adds it to the active list.
        if room not in self.active_rooms:
            self.active_rooms[room] = []
        self.active_rooms[room].append(websocket)
        asyncio.create_task(self.listen_redis(room))  # Start listening for room messages

    def disconnect(self, room: str, websocket: WebSocket):
        self.active_rooms[room].remove(websocket)
        if not self.active_rooms[room]:  # If room is empty, delete it
            del self.active_rooms[room]

    async def broadcast(self, room: str, message: str):
        redis_pubsub.publish(room, message)  #Sends a message to all WebSocket clients in a specific room.

    async def listen_redis(self, room: str):
        async for message in redis_pubsub.subscribe(room): #Listens to Redis and forwards messages to WebSocket clients.
            for connection in self.active_rooms.get(room, []):
                await connection.send_text(message)


connection_manager = ConnectionManager() #create instance of the class