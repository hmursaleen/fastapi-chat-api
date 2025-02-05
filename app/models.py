from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str
    password: str



class Message(BaseModel):
    room: str
    sender: str
    content: str
    timestamp: Optional[datetime] = None
