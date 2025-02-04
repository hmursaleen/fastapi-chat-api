import redis
import asyncio
from app.config import REDIS_HOST, REDIS_PORT

'''
To understand what Redis pub/sub is: https://medium.com/redis-with-raphael-de-lio/understanding-pub-sub-in-redis-18278440c2a9

The following class:
    Each room gets its own Redis channel for isolation.
    Uses async generator (yield) for efficient streaming.
'''

class RedisPubSub:
    
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def publish(self, room: str, message: str):
        self.redis.publish(room, message) #Publish a message to a room.

    async def subscribe(self, room: str):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(room) #Subscribe to a Redis room and listens for messages.
        
        async for message in self._listen(pubsub):
            yield message["data"]

    async def _listen(self, pubsub): #Helper function to asynchronously listen for messages.
        
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                yield message
            await asyncio.sleep(0.1)


redis_pubsub = RedisPubSub() # Create a shared RedisPubSub instance