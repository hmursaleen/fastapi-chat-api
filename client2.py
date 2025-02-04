import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected as Client 2")
        await websocket.send("Hello from Client 2!")

        while True:
            response = await websocket.recv()
            print(f"Client 2 received: {response}")

asyncio.run(test_websocket())