from pydantic import BaseModel, Field, PositiveInt, HttpUrl
from ..valueobjects.enums import MovieGenre, MovieRating
from typing import Optional
from datetime import datetime, date

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., max_length=200)
    original_title: Optional[str] = Field(None, max_length=200)
    minute_duration: PositiveInt = Field(..., help_text="Duration in minutes")
    release_date: date
    end_date: date
    description: str
    genre: MovieGenre
    rating: MovieRating
    poster_url: Optional[HttpUrl] = None 
    trailer_url: Optional[HttpUrl] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
