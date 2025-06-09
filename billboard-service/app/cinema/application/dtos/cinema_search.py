from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.cinema.domain.enums import CinemaStatus, CinemaType, LocationRegion

class CinemaSearchFilters(BaseModel):
    name: Optional[str] = None
    tax_number: Optional[str] = None
    is_active: Optional[bool] = None
    min_screens: Optional[int] = None
    max_screens: Optional[int] = None
    type: Optional[CinemaType] = None
    status: Optional[CinemaStatus] = None
    region: Optional[LocationRegion] = None
    has_parking: Optional[bool] = None
    has_food_court: Optional[bool] = None
    renovated_after: Optional[date] = None
    renovated_before: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email_contact: Optional[str] = None

class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10
