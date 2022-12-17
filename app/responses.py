from pydantic import BaseModel
from typing import Optional, Literal

# Responses Schemas
class PostAuth(BaseModel):
    username: str
    password: str

class PostTeam(BaseModel):
    name: str

class PostPlayer(BaseModel):
    name: str
    birthdate: str
    weight: float
    height: int
    role: Literal['coach', 'player']

class UpdatePlayer(BaseModel):
    name: Optional[str]
    birthdate: Optional[str]
    weight: Optional[float]
    height: Optional[int]
    role: Optional[Literal['coach', 'player']]
