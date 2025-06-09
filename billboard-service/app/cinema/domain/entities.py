from pydantic import Field
from .base import CinemaBase

class Cinema(CinemaBase):
    """Domain model representing a cinema with all required fields"""
    id: int = Field(..., description="Unique identifier for the cinema")