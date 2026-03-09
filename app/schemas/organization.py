from pydantic import BaseModel, Field
from typing import List, Optional
import phonenumbers
from phonenumbers import PhoneNumberFormat


class PhoneNumberValidator(BaseModel):
    number: str = Field(..., description="Phone number")

    @classmethod
    def validate_phone(cls, v: str) -> str:
        try:
            parsed = phonenumbers.parse(v, "RU")
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            return phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format")


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Organization name")
    building_id: int = Field(..., description="Building ID")
    phone_numbers: List[str] = Field(default_factory=list, description="List of phone numbers")
    activity_ids: List[int] = Field(default_factory=list, description="List of activity IDs")


class OrganizationResponse(BaseModel):
    id: int
    name: str
    building_id: int
    phone_numbers: List[str]
    activities: List[dict]

    class Config:
        from_attributes = True


class OrganizationSearch(BaseModel):
    name: Optional[str] = Field(None, description="Search by organization name")
    activity_id: Optional[int] = Field(None, description="Filter by activity ID")
    building_id: Optional[int] = Field(None, description="Filter by building ID")
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude for nearby search")
    lon: Optional[float] = Field(None, ge=-180, le=180, description="Longitude for nearby search")
    radius_km: Optional[float] = Field(None, gt=0, description="Radius in kilometers for nearby search")