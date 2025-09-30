from pydantic import BaseModel
from typing import Optional

class ApiResponse(BaseModel):
    """통일된 API 응답 모델"""
    success: bool
    message: str = ""
    data: Optional[dict] = None
