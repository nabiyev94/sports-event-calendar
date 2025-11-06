from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class EventCreate(BaseModel):
    sport: str = Field(..., examples=["Football"])
    home_team: str = Field(..., examples=["Salzburg"])
    opponent_team: str = Field(..., examples=["Sturm"])
    starts_at: datetime = Field(..., examples=["2025-07-18T18:30:00+02:00"])
    venue: str | None = Field(default=None, examples=["Red Bull Arena"])
    city: str | None = Field(default=None, examples=["Salzburg"])
    country: str | None = Field(default=None, examples=["AT"])
    description: str | None = None

class EventOut(BaseModel):
    id: int
    sport: str
    home_team: str
    opponent_team: str
    venue: str | None
    city: str | None
    country: str | None
    starts_at: datetime
    description: str | None

    model_config = ConfigDict(from_attributes=True)