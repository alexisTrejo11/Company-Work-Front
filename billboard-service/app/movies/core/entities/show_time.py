from datetime import datetime
from pydantic import Field, BaseModel
from decimal import Decimal
from typing import Optional

class Showtime(BaseModel):
    """
    Represents a Showtime entity for a Movie in a Theater.
    """
    id: Optional[int] = None
    movie_id: int
    theater_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    price: Decimal = Field(..., max_digits=6, decimal_places=2)