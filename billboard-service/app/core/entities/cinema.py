from enum import Enum
from pydantic import BaseModel, Field, EmailStr, HttpUrl, PositiveInt, root_validator, validator
from typing import Optional, List
from datetime import datetime

class Cinema(BaseModel):
    """
    Represents a Cinema Entity
    """
    id: Optional[int] = None
    name: str = Field(..., max_length=20)
    email: EmailStr
    #tax_number = str = Field(..., max_length=20),
    is_active: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
