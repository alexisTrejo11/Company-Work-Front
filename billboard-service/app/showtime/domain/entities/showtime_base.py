from pydantic import Field, BaseModel, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..enums import ShowtimeLanguage, ShowtimeType

class ShowtimeBase(BaseModel):
    """Base schema for common Showtime attributes."""
    movie_id: int
    cinema_id: int
    theater_id: int
    price: Decimal = Field(..., max_digits=6, decimal_places=2)
    start_time: datetime
    end_time: Optional[datetime] = None 
    type: ShowtimeType
    language: ShowtimeLanguage

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
