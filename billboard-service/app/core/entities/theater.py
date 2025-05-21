from pydantic import BaseModel
from typing import Optional
from pydantic import PositiveInt, Field
from ..valueobjects.enums import TheaterType 

class Theather(BaseModel):
    """
    Represents a Theater entity within a Cinema.
    """
    id: Optional[int] = None
    cinema_id: int
    name: str = Field(..., max_length=50)
    capacity: PositiveInt
    theater_type: TheaterType
    is_active: bool = True
    maintenance_mode: bool = False

    class Config:
        orm_mode = True
