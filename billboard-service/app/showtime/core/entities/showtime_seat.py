from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class ShowtimeSeatBase(BaseModel):
    """
    Base schema for ShowtimeSeat, containing common attributes.
    """
    showtime_id: int = Field(..., description="The ID of the showtime this seat belongs to.")
    theater_seat_id: int = Field(..., description="The ID of the specific theater seat.")
    
    taken_at: Optional[datetime] = Field(None, description="Timestamp when the seat was taken/booked.")
    user_id: Optional[int] = Field(None, description="The ID of the user who took this seat.")

class ShowtimeSeatEntity(ShowtimeSeatBase):
    """
    Full domain entity for a ShowtimeSeat, including database-generated fields.
    'id' is Optional when created before persistence.
    """
    id: Optional[int] = Field(None, description="The unique identifier of the showtime seat.")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the seat record was created.")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the seat record was last updated.")

    def is_taken(self) -> bool:
        return self.taken_at is not None 

    def take(self):
        if self.is_taken():
            raise ValueError("Seat Already Taken")
        self.taken_at = datetime.now(timezone.utc())

    def leave(self):
        self.taken_at = None
        self.user_id = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "showtime_id": 101,
                "theater_seat_id": 205,
                "taken_at": "2025-06-06T14:00:00Z",
                "transaction_id": 5001,
                "user_id": 123,
                "created_at": "2025-06-06T13:30:00Z",
                "updated_at": "2025-06-06T13:30:00Z"
            }
        }