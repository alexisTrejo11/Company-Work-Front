from datetime import date
from typing import Optional, List, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.cinema.domain.enums import CinemaType, CinemaStatus, CinemaFeatures, LocationRegion
from app.cinema.domain.value_objects import CinemaAmenities, ContactInfo, Location, SocialMedia
from app.cinema.domain.base import CinemaBase

class CinemaCreate(CinemaBase):
    """Model for creating new cinemas (all fields required except ID)"""
    pass


class CinemaUpdate(BaseModel):
    """Model for partial updates with all optional fields"""
    model_config = ConfigDict(
        extra='forbid',
        json_encoders={date: lambda v: v.isoformat()}
    )

    image: Optional[str] = Field(None, description="URL or path to the cinema's main image.")
    name: Optional[str] = Field(None, max_length=255, min_length=3, description="Name of the cinema.")
    tax_number: Optional[str] = Field(None, max_length=255, min_length=5, description="Tax ID number.")
    is_active: Optional[bool] = Field(None, description="Operational status flag.")
    description: Optional[str] = Field(None, description="Brief description.")
    screens: Optional[int] = Field(None, ge=0, description="Number of screens.")
    last_renovation: Optional[date] = Field(None, description="Last renovation date.")

    type: Optional[CinemaType] = Field(None, description="Type of cinema.")
    status: Optional[CinemaStatus] = Field(None, description="Operational status.")
    amenities: Optional[CinemaAmenities] = Field(None, description="Amenities details.")
    region: Optional[LocationRegion] = Field(None, description="Region location.")

    contact_info: Optional[ContactInfo] = Field(None, description="Contact information.")
    location: Optional[Location] = Field(None, description="Geographical coordinates.")
    social_media: Optional[SocialMedia] = Field(None, description="Social media links.")
    features: Optional[List[CinemaFeatures]] = Field(None, description="Special features.")

    @field_validator('last_renovation')
    @classmethod
    def validate_last_renovation_not_future(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v > date.today():
            raise ValueError('Last renovation date cannot be in the future.')
        return v

    def dict(self, exclude_none=True, **kwargs) -> dict[str, Any]:
        """Override dict to exclude None values by default for partial updates"""
        return super().model_dump(exclude_none=exclude_none, **kwargs)