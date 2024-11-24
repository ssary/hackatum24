from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class UserGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NONE_BINARY = "none-binary"

class UserModel(BaseModel):
    userId: str
    name: str
    avatarUrl: str
    age: int
    gender: UserGender
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)