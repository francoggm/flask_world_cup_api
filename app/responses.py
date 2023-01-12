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
    position: str
    games_played: int
    minutes_played: int
    cards_yellow: int
    cards_red: int
    goals: int

class UpdatePlayer(BaseModel):
    name: Optional[str]
    birthdate: Optional[str]
    weight: Optional[float]
    height: Optional[int]
    position: Optional[str]
    games_played: Optional[int]
    minutes_played: Optional[int]
    cards_yellow: Optional[int]
    cards_red: Optional[int]
    goals: Optional[int]
