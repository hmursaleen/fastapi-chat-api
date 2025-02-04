from fastapi import WebSocket, WebSocketDisconnect
from typing import List

'''
The following class:
    Implements a Connection Manager to handle multiple users.
    Stores connected users and broadcasts messages efficiently.
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
        for connection in self.active_connections: #Sends a message to all connected clients.
            await connection.send_text(message)


connection_manager = ConnectionManager() #create instance of the class
