from datetime import date
from typing import Annotated, Optional
from fastapi import Query
from app.cinema.core.entities.valueobjects import LocationRegionEnum
from app.cinema.infrastructure.persistence.model.cinema_model import CinemaStatusEnum, CinemaTypeEnum
from pydantic import BaseModel

class CinemaSearchFilters(BaseModel):
    name: Optional[str] = None
    tax_number: Optional[str] = None
    is_active: Optional[bool] = None
    min_screens: Optional[int] = None
    max_screens: Optional[int] = None
    type: Optional[CinemaTypeEnum] = None
    status: Optional[CinemaStatusEnum] = None
    region: Optional[LocationRegionEnum] = None
    has_parking: Optional[bool] = None
    has_food_court: Optional[bool] = None
    renovated_after: Optional[date] = None
    renovated_before: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email_contact: Optional[str] = None


class CinemaSearchQuery(BaseModel):
    name: Annotated[Optional[str], Query()] = None,
    tax_number: Annotated[Optional[str], Query()] = None,
    is_active: Annotated[Optional[bool], Query()] = None,
    min_screens: Annotated[Optional[int], Query(ge=0)] = None,
    max_screens: Annotated[Optional[int], Query(ge=0)] = None,
    type: Annotated[Optional[CinemaTypeEnum], Query()] = None,
    status: Annotated[Optional[CinemaStatusEnum], Query()] = None,
    region: Annotated[Optional[LocationRegionEnum], Query()] = None,
    has_parking: Annotated[Optional[bool], Query()] = None,
    has_food_court: Annotated[Optional[bool], Query()] = None,
    renovated_after: Annotated[Optional[date], Query()] = None,
    renovated_before: Annotated[Optional[date], Query()] = None,
    latitude: Annotated[Optional[float], Query()] = None,
    longitude: Annotated[Optional[float], Query()] = None,
    phone: Annotated[Optional[str], Query()] = None,
    email_contact: Annotated[Optional[str], Query()] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10

class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10
