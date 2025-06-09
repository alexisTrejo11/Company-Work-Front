from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from app.showtime.domain.entities.showtime import ShowtimeBase
from app.showtime.domain.enums import ShowtimeLanguage, ShowtimeType

class ShowtimeCreate(ShowtimeBase):
    """Schema for creating a new Showtime. No ID or timestamps."""
    pass

class ShowtimeUpdate(BaseModel):
    """Schema for updating an existing Showtime. All fields optional for partial updates."""
    id: int = Field(..., description="The ID of the showtime to update.") # Required for update
    movie_id: Optional[int] = None
    theater_id: Optional[int] = None
    price: Optional[Decimal] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    type: Optional[ShowtimeType] = None
    language: Optional[ShowtimeLanguage] = None

    @field_validator('start_time')
    @classmethod
    def validate_start_time_timezone(cls, v):
        if v.tzinfo is None:
            raise ValueError('start_time must include time zone information')
        return v
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time_timezone(cls, v):
        if v is not None and v.tzinfo is None:
            raise ValueError('end_time must include time zone information')
        return v