from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from app.redis_pubsub import redis_pubsub
import asyncio

'''
The following class:
    Implements a Connection Manager to handle multiple users.
    Stores connected users and broadcasts messages efficiently.
    Uses Redis Pub/Sub to relay messages instead of local broadcasting.
    Implements async listening to receive messages in real-time.
'''
class ConnectionManager:
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept() #Accepts a WebSocket connection and adds it to the active list.
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket) #Removes a disconnected WebSocket connection

    async def broadcast(self, message: str):
        redis_pubsub.publish("chat_channel", message)  # Sends a message to all connected clients by publishing it to a Redis channel

    async def listen_redis(self):
        async for message in redis_pubsub.subscribe("chat_channel"): #Listens to Redis and forwards messages to WebSocket clients.
            for connection in self.active_connections:
                await connection.send_text(message)


connection_manager = ConnectionManager() #create instance of the class