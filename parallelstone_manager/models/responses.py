from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class CommandResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None  
    timestamp: datetime = datetime.now()
