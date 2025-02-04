from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.websocket import connection_manager as ws_conn #the instance of ConnectionManager class
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Chat API"}


'''
The following function:
    Creates a background task to listen to Redis (asyncio.create_task).
    Handles disconnections properly.
'''
@app.websocket("/ws") #Clients connect to ws://localhost:8000/ws
async def websocket_endpoint(websocket: WebSocket):
    await ws_conn.connect(websocket)

    asyncio.create_task(ws_conn.listen_redis()) #start listening to Redis channel
    
    try:
        while True:
            data = await websocket.receive_text()
            await ws_conn.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        ws_conn.disconnect(websocket)
        await ws_conn.broadcast("A client has disconnected.") #When a client disconnects, it notifies others



'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
'''
