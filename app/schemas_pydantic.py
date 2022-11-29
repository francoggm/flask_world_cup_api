from pydantic import BaseModel
from typing import Optional

# Response Schemas
class PostAuth(BaseModel):
    username: str
    password: str

class PostUser(BaseModel):
    pass

class PostTeam(BaseModel):
    name: str
    created: str

class PostPlayer(BaseModel):
    name: str
    birthdate: str
    weight: float
    height: int

class PostCoach(BaseModel):
    name: str 
    birthdate: str

class UpdateUser(BaseModel):
    pass

class UpdateTeam(BaseModel):
    name: Optional[str]
    created_date: Optional[str]

class UpdatePlayer(BaseModel):
    name: Optional[str]
    birthdate: Optional[str]
    weight: Optional[float]
    height: Optional[int]

class UpdateCoach(BaseModel):
    name: Optional[str]
    birthdate: Optional[str]