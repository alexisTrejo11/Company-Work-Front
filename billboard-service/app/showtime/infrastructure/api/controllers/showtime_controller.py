from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, status
from ....core.entities.showtime import Showtime
from ....application.use_cases.showtime_command_use_cases import ScheduleShowtimeUseCase, UpdateShowtimeUseCase, DeleteShowtimeUseCase
from ....application.use_cases.showtime_query_use_cases import GetShowtimeByIdUseCase, GetShowtimesUseCase
from ...injection.depdencies import schedule_showtime_use_case, update_showtime_use_case, delete_showtime_use_case, get_showtime_by_id_use_case, get_showtimes_use_case
from ....application.dtos.showtime_dtos import ShowtimeCreate, ShowtimeUpdate

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

@router.post("/", response_model=Showtime, status_code=status.HTTP_201_CREATED)
async def create_showtime(
    showtime_data: ShowtimeCreate,
    use_case: ScheduleShowtimeUseCase = Depends(schedule_showtime_use_case)
):
    return await use_case.execute(showtime_data)

@router.put("/{showtime_id}", response_model=Showtime)
async def update_showtime(
    showtime_id: int,
    update_data: ShowtimeUpdate,
    use_case: UpdateShowtimeUseCase = Depends(update_showtime_use_case)
):
    return await use_case.execute(showtime_id, update_data)

@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_showtime(
    showtime_id: int,
    use_case: DeleteShowtimeUseCase = Depends(delete_showtime_use_case)
):
    await use_case.execute(showtime_id)


