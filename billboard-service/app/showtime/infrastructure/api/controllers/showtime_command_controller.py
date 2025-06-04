from fastapi import APIRouter, Depends, status
from ....core.entities.show_time import Showtime
from ....application.use_cases.showtime_command_use_cases import (
    ScheduleShowtimeUseCase, UpdateShowtimeUseCase, DeleteShowtimeUseCase,
)
from ...injection.depdencies import (
    schedule_showtime_use_case, update_showtime_use_case, delete_showtime_use_case,
)

router = APIRouter(prefix="/api/v1/showtimes", tags=["showtimes"])

@router.post("/", response_model=Showtime, status_code=status.HTTP_201_CREATED)
async def create_showtime(
    showtime_data: dict,
    use_case: ScheduleShowtimeUseCase = Depends(schedule_showtime_use_case)
):
    return await use_case.execute(showtime_data)

@router.put("/{showtime_id}", response_model=Showtime)
async def update_showtime(
    showtime_id: int,
    update_data: dict,
    use_case: UpdateShowtimeUseCase = Depends(update_showtime_use_case)
):
    return await use_case.execute(showtime_id, update_data)

@router.delete("/{showtime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_showtime(
    showtime_id: int,
    use_case: DeleteShowtimeUseCase = Depends(delete_showtime_use_case)
):
    await use_case.execute(showtime_id)
