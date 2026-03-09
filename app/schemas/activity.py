from pydantic import BaseModel, Field
from typing import Optional, List


class ActivityCreate(BaseModel):
    name: str = Field(..., description="Activity name")
    parent_id: Optional[int] = Field(None, description="Parent activity ID")


class ActivityResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    level: int
    children: List['ActivityResponse'] = []

    class Config:
        from_attributes = True


ActivityResponse.model_rebuild()