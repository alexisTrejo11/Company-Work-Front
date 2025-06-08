from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from ...core.entities.showtime import ShowtimeBase
from ...core.entities.value_objects import ShowtimeLanguage, ShowtimeType


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