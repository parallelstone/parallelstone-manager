from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Player(BaseModel):
    name: str
    uuid: str
    joined_at: datetime
    ping: Optional[int] = None 

class PlayerListResponse(BaseModel):
    players: List[Player] 
    total_count: int
