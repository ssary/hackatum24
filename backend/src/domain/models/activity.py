from pydantic import BaseModel, Field
from datetime import datetime
from src.domain.models.user import UserModel
from src.domain.models.message import MessageModel

class ActivityLocation(BaseModel):
    lon: float
    lat: float
    radius: float
    name: str = "Default Location"

class ActivityTimerange(BaseModel):
    startTime: datetime
    endTime: datetime

class ActivityModel(BaseModel):
    description: str
    minUsers: int
    maxUsers: int
    timerange: ActivityTimerange
    location: ActivityLocation
    joinedUsers: list[UserModel] = []
    messages: list[MessageModel] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
