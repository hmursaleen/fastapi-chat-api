import os
from dotenv import load_dotenv 
from motor.motor_asyncio import AsyncIOMotorClient #Uses Motor for asynchronous MongoDB operations.

# Load environment variables
load_dotenv()

#Configure Redis Connection
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


#For JWT Token system
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#mongodb connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = "chat_db"

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]
messages_collection = db["messages"]  # Collection for chat messages
