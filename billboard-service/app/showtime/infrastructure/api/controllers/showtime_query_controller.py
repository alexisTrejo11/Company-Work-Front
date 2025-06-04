from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from ....core.entities.show_time import Showtime
from ....application.use_cases.showtime_query_use_cases import (
    GetShowtimeByIdUseCase, GetShowtimesUseCase,
    GetIncomingShowtimesByMovieUseCase, GetIncomingShowtimesByCinemaUseCase
)
from ...injection.depdencies import (
    get_showtime_by_id_use_case, get_showtimes_use_case,
    get_incoming_showtime_by_cinema_use_case, get_incoming_showtime_by_movie_use_case,
)

router = APIRouter(prefix="/api/v1/showtimes", tags=["showtimes"])

@router.get("/{showtime_id}", response_model=Showtime)
async def get_showtime(
    showtime_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(get_showtime_by_id_use_case)
):
    showtime = await use_case.execute(showtime_id)
    return showtime

@router.get("/", response_model=List[Showtime])
async def get_showtimes(
    movie_id: Optional[int] = None,
    theater_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    start_time_after: Optional[datetime] = None,
    end_time_before: Optional[datetime] = None,
    use_case: GetShowtimesUseCase = Depends(get_showtimes_use_case)
):
    filters = {}
    if movie_id is not None:
        filters["movie_id"] = movie_id
    if theater_id is not None:
        filters["theater_id"] = theater_id
    if is_active is not None:
        filters["is_active"] = is_active
    if start_time_after is not None:
        filters["start_time_after"] = start_time_after
    if end_time_before is not None:
        filters["end_time_before"] = end_time_before
    
    showtimes = await use_case.execute(filters=filters)
    if not showtimes:
        return []
    
    return showtimes


@router.get("/incoming/movie/{movie_id}", response_model=Showtime)
async def get_incoming_showtimes_by_movie(
    movie_id: int,
    use_case: GetIncomingShowtimesByMovieUseCase = Depends(get_incoming_showtime_by_movie_use_case)
):
    showtimes = await use_case.execute(movie_id)
    if not showtimes:
        return []
    
    return showtimes

@router.get("/incoming/cinema/{cinema_id}", response_model=Showtime)
async def get_incoming_showtimes_by_cinema(
    cinema_id: int,
    use_case: GetIncomingShowtimesByCinemaUseCase = Depends(get_incoming_showtime_by_cinema_use_case)
):
    showtimes = await use_case.execute(cinema_id)
    if not showtimes:
        return []
    
    return showtimes

