from typing import List
from fastapi import APIRouter, Depends, status
from ....application.use_cases.seats_use_cases import (
    GetTheaterSeatByIdUseCase,
    GetSeatsByTheaterUseCase,
    SaveTheaterSeatUseCase,
    DeleteTheaterSeatUseCase
)
from ....core.entities.seat import TheaterSeatEntity
from ...injection.theater_seat_dependencies import (
    get_seats_by_theater_use_case, get_theater_seat_by_id_use_case,
    save_theater_seat_use_case, delete_theater_seat_use_case,
)

router = APIRouter(prefix="/api/v1/theaters/seats", tags=["Theater Seats"])

@router.post(
    "/",
    response_model=TheaterSeatEntity,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new theater seat"
)
async def create_theater_seat(
    new_seat: TheaterSeatEntity,
    use_case: SaveTheaterSeatUseCase = Depends(save_theater_seat_use_case)
) -> TheaterSeatEntity:
    """
    Creates a new theater seat record.
    """
    created_seat = await use_case.execute(new_seat)
    return created_seat

@router.get(
    "/{seat_id}",
    response_model=TheaterSeatEntity,
    summary="Get a theater seat by ID"
)
async def get_theater_seat_by_id(
    seat_id: int,
    use_case: GetTheaterSeatByIdUseCase = Depends(get_theater_seat_by_id_use_case)
) -> TheaterSeatEntity:
    """
    Retrieves a single theater seat by its unique ID.
    Raises a 404 Not Found error if the seat does not exist.
    """
    seat = await use_case.execute(seat_id)
    return seat

@router.get(
    "/by_theater/{theater_id}", # /theaters/{theater_id}/seats
    response_model=List[TheaterSeatEntity],
    summary="Get all seats for a specific theater"
)
async def get_seats_by_theater(
    theater_id: int,
    use_case: GetSeatsByTheaterUseCase = Depends(get_seats_by_theater_use_case)
) -> List[TheaterSeatEntity]:
    """
    Retrieves a list of all theater seats associated with a specific theater ID.
    """
    seats = await use_case.execute(theater_id)
    return seats

@router.put(
    "/{seat_id}",
    response_model=TheaterSeatEntity,
    summary="Update an existing theater seat"
)
async def update_theater_seat(
    seat_id: int,
    updated_seat: TheaterSeatEntity,
    use_case: SaveTheaterSeatUseCase = Depends(save_theater_seat_use_case)
) -> TheaterSeatEntity:
    """
    Updates an existing theater seat record identified by its ID.
    Only provided fields in the request body will be updated.
    Raises a 404 Not Found error if the seat does not exist.
    """
    # TODO: Refactor/ Separate
    updated_seat.id = seat_id

    updated_seat = await use_case.execute(updated_seat)
    return updated_seat

@router.delete(
    "/{seat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a theater seat by ID"
)
async def delete_theater_seat(
    seat_id: int,
    use_case: DeleteTheaterSeatUseCase = Depends(delete_theater_seat_use_case)
) -> None:
    """
    Deletes a theater seat record by its unique ID.
    Returns 204 No Content on successful deletion.
    Raises a 404 Not Found error if the seat does not exist before attempting deletion.
    """
    await use_case.execute(seat_id)
    return 