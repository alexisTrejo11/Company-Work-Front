from enum import Enum
from pydantic import BaseModel


class Seats(BaseModel):
    seat_id: str
    is_taken: bool = False