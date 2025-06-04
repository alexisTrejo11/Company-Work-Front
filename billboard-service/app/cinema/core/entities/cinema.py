from datetime import date
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from .valueobjects import (
    ContactInfo, Location, CinemaFeatures, 
    CinemaAmenities, CinemaType, CinemaStatus,
    SocialMedia
)

class Cinema(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the cinema (optional for creation).")
    image: str = Field('', description="URL or path to the cinema's main image.")
    name: str = Field(..., max_length=255, min_length=3, description="Name of the cinema.")
    tax_number: str = Field(..., max_length=255, min_length=5, description="Unique tax identification number of the cinema.")
    is_active: bool = Field(False, description="True if the cinema is currently operational and accepting bookings.")
    description: str = Field('', description="A brief description of the cinema.")
    screens: int = Field(..., ge=0, description="Number of screens/theaters in the cinema.")
    last_renovation: Optional[date] = Field(None, description="Date of the last major renovation.")

    type: CinemaType = Field(..., description="Type of cinema (e.g., VIP, Traditional).")
    status: CinemaStatus = Field(..., description="Current operational status of the cinema.")
    amenities: CinemaAmenities = Field(..., description="Details about amenities available at the cinema.")

    contact_info: ContactInfo = Field(..., description="Contact information for the cinema.")
    location: Location = Field(..., description="Geographical location coordinates of the cinema.")
    social_media: SocialMedia = Field(..., description="Social media links for the cinema.")
    features: List[CinemaFeatures] = Field(..., description="List of special features offered by the cinema (e.g., 3D, IMAX).")

    @field_validator('last_renovation')
    @classmethod
    def validate_last_renovation_not_future(cls, v: Optional[date]) -> Optional[date]:
        """Ensures the last renovation date is not in the future."""
        if v is not None and v > date.today():
            raise ValueError('Last renovation date cannot be in the future.')
        return v
    

    class Config:
        orm_mode = True
        use_enum_values = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }
