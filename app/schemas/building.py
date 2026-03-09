from pydantic import BaseModel, Field
from typing import List


class BuildingCreate(BaseModel):
    address: str = Field(..., description="Building address")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")


class BuildingResponse(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True