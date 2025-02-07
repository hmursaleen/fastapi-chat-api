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
        #This creates a connection to the Redis server

    def pub(self, room: str, message: str):
        self.redis.publish(room, message)
        #This uses the Redis connection (self.redis) to publish the message to the specified channel

    async def sub(self, room: str):
        pubsub = self.redis.pubsub() 
        #This creates a Pub/Sub object using the pubsub() method of the Redis connection.
        #self.pubsub is an attribute that allows you to subscribe to channels and listen for messages.
        pubsub.subscribe(room) #Subscribe to a Redis room and listens for messages.
        
        async for message in self._listen(pubsub):
            yield message["data"]
            '''
            This uses the yield keyword to return the message data to the caller. yield makes this method a generator, 
            which can produce a sequence of values over time.

            message["data"] accesses the data field of the message, which contains the actual content of the message. 
            This field is provided by Redis when a message is received. You don’t need to declare data yourself.
            '''

    async def _listen(self, pubsub): #Helper function to asynchronously listen for messages.
        
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                yield message
            await asyncio.sleep(0.1)
            '''
            This pauses the loop for 0.1 seconds before checking for new messages again. It prevents the loop from consuming too much CPU.
            '''


redis_pubsub = RedisPubSub() # Create a shared RedisPubSub instance