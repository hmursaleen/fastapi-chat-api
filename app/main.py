from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.websocket import connection_manager as ws_conn #the instance of ConnectionManager class

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chat API"}


'''
The following function:
    Each WebSocket connection must specify a room in the URL.
    Users only receive messages from their room.
'''

#message showing twice to each user

@app.websocket("/ws/{room}") #Clients connect to ws://localhost:8000/ws/room
async def websocket_endpoint(room: str, websocket: WebSocket):
    await ws_conn.connect(room, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await ws_conn.broadcast(room, f"[{room}] {data}")
    except WebSocketDisconnect:
        ws_conn.disconnect(room, websocket)
        await ws_conn.broadcast(room, f"[{room}] A user has left the chat.") #When a client disconnects, it notifies others