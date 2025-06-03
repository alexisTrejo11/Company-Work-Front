from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from ....core.entities.show_time import Showtime
from ....application.use_cases.show_time_use_cases import (
    GetShowtimeByIdUseCase,
    ListShowtimesUseCase,
)
from ...injection.depdencies import (
    get_showtime_by_id_use_case,
    list_showtimes_use_case,
)

router = APIRouter(prefix="/api/v1/showtimes", tags=["showtimes"])

@router.get("/{showtime_id}", response_model=Showtime)
async def get_showtime(
    showtime_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(get_showtime_by_id_use_case)
):
    showtime = await use_case.execute(showtime_id)
    if not showtime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    return showtime

@router.get("/", response_model=List[Showtime])
async def list_showtimes(
    movie_id: Optional[int] = None,
    theater_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    start_time_after: Optional[datetime] = None,
    end_time_before: Optional[datetime] = None,
    use_case: ListShowtimesUseCase = Depends(list_showtimes_use_case)
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
    
    return await use_case.execute(filters=filters)

#TODO: MAKE THIS LIST BY
@router.get("/incoming/movie/{movie_id}", response_model=Showtime)
async def list_incoming_showtimes_by_movie(
    movie_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(get_showtime_by_id_use_case)
):
    showtime = await use_case.execute(movie_id)
    return showtime

@router.get("/incoming/cinema/{cinema_id}", response_model=Showtime)
async def list_incoming_showtimes_by_cinema(
    cinema_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(get_showtime_by_id_use_case)
):
    showtime = await use_case.execute(cinema_id)
    return showtime


@router.get("/incoming/cinema/{cinema_id}", response_model=Showtime)
async def list_incoming_showtimes_by_theater(
    cinema_id: int,
    use_case: GetShowtimeByIdUseCase = Depends(get_showtime_by_id_use_case)
):
    showtime = await use_case.execute(cinema_id)
    return showtime



