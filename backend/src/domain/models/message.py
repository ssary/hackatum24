from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.domain.models.user import UserModel

class MessageModel(BaseModel):
    content: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # user: Optional[UserModel] = None