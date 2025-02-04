import redis
import asyncio
from app.config import REDIS_HOST, REDIS_PORT

'''
To understand what Redis pub/sub is: https://medium.com/redis-with-raphael-de-lio/understanding-pub-sub-in-redis-18278440c2a9

The following class:
    Implements publish-subscribe pattern using Redis.
    Uses yield for efficient message streaming.
'''

class RedisPubSub:
    
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.pubsub = self.redis.pubsub()

    def publish(self, channel: str, message: str):
        self.redis.publish(channel, message) #Publish a message to a channel.

    async def subscribe(self, channel: str):
        self.pubsub.subscribe(channel) #Subscribe to a Redis channel and listens for messages.
        while True:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                yield message["data"]
            await asyncio.sleep(0.1)


redis_pubsub = RedisPubSub() # Create a shared RedisPubSub instance
