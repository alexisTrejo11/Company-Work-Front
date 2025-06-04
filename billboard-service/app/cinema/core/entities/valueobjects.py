from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactInfo(BaseModel):
    address: str
    phone: str
    email_contact: EmailStr
    location: dict 

class Location(BaseModel):
    lat: float
    lng: float

class SocialMedia(BaseModel):
    facebook: Optional[str]
    instagram: Optional[str]
    x: Optional[str]
    tik_tok: Optional[str]

class CinemaStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    MAINTENANCE = "MAINTENANCE"

class CinemaFeatures(Enum):
    TWO_D = "2D"
    THREE_D = "3D"
    FOUR_D = "4D"
    IMAX = "IMAX"
    VIP_SEATING = "VIP_SEATING"
    DOBLY_ATMOS = "DOBLY_ATMOS"


class CinemaType(Enum):
    VIP = "VIP"
    TRADITIONAL = "TRADITIONAL"

class CinemaAmenities(BaseModel):
    parking: bool = False
    food_court: bool = False
    coffee_station: bool = False
    disabled_access: bool = False
