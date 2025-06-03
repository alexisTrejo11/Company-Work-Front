from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from ....application.use_cases.show_time_use_cases import (
    GetShowtimeByIdUseCase,
    ListShowtimesUseCase,
    CreateShowtimeUseCase,
    UpdateShowtimeUseCase,
    DeleteShowtimeUseCase,
    GetAvailableShowtimesUseCase
)
from ...injection.depdencies import (
    get_showtime_by_id_use_case,
    list_showtimes_use_case,
    create_showtime_use_case,
    update_showtime_use_case,
    delete_showtime_use_case,
    get_available_showtimes_use_case
)
from ....core.entities.show_time import Showtime

router = APIRouter(prefix="/api/v1/showtimes", tags=["showtimes"])

@router.post("/", response_model=Showtime, status_code=status.HTTP_201_CREATED)
async def create_showtime(
    showtime_data: dict,
    use_case: CreateShowtimeUseCase = Depends(create_showtime_use_case)
):
    try:
        return await use_case.execute(showtime_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{showtime_id}", response_model=Showtime)
async def update_showtime(
    showtime_id: int,
    update_data: dict,
    use_case: UpdateShowtimeUseCase = Depends(update_showtime_use_case)
):
    try:
        return await use_case.execute(showtime_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_showtime(
    showtime_id: int,
    use_case: DeleteShowtimeUseCase = Depends(delete_showtime_use_case)
):
    try:
        await use_case.execute(showtime_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/available/", response_model=List[Showtime])
async def get_available_showtimes(
    movie_id: Optional[int] = None,
    theater_id: Optional[int] = None,
    use_case: GetAvailableShowtimesUseCase = Depends(get_available_showtimes_use_case)
):
    return await use_case.execute(movie_id=movie_id, theater_id=theater_id)