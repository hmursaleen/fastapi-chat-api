import asyncio
import websockets

'''
What this does:

Connects to the WebSocket server.
Sends a message ("Hello from Client 1!").
Continuously listens for incoming messages.
'''

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected as Client 1")
        await websocket.send("Hello from client1!")
        while True:
            response = await websocket.recv()
            print(f"Client 1 received: {response}")

asyncio.run(test_websocket())
