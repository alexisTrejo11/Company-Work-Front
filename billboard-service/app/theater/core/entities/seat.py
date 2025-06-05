from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ..valueobjects.enums import SeatType

class TheaterSeatEntity(BaseModel):
    """
    Base schema for TheaterSeat, containing common attributes for creation/update.
    """
    id: Optional[int] = Field(..., description="The ID of the seat")
    theater_id: int = Field(..., description="The ID of the theater this seat belongs to.")
    seat_row: str = Field(..., max_length=5, description="The row identifier of the seat (e.g., 'A', 'AA', 'SEC1').")
    seat_number: int = Field(..., gt=0, description="The number of the seat within its row.")
    seat_type: SeatType = Field(SeatType.STANDARD, description="The classification type of the seat (e.g., STANDARD, VIP, ACCESSIBLE).")
    is_active: bool = Field(True, description="Indicates if the seat is currently active and usable.")

