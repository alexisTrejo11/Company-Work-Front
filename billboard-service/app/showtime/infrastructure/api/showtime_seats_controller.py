from fastapi import APIRouter
from ...domain.entities.showtime_seat import ShowtimeSeatEntity as ShowtimeSeat
from ...application.use_cases.showtime_seats_use_case import GetShowtimeSeatsUseCase

router = APIRouter(prefix="/api/v1/showtimes")

@router.get("{showtime_id}/seats" , response_model=ShowtimeSeat, tags=['Showtime Seats'])
def get_showtime_seat_disponibility(
    showtime_id: int,
    usecase : GetShowtimeSeatsUseCase
):
    showtime_seats = usecase.execute(showtime_id)
    return showtime_seats

@router.get("/seats/{seat_id}", response_model=ShowtimeSeat, tags=['Showtime Seats'])
def get_showtime_seat(
    seat_id: int,
    usecase
):
    showtime_seat = usecase.execute(seat_id)
    return showtime_seat

#TODO: MANY
@router.patch("/seats/{seat_id}/take", response_model=ShowtimeSeat, tags=['Showtime Seats'])
def take_seats(
    take_seat_data: dict,
    seat_id: int,
    usecase
):
    showtime_seat = usecase.execute(seat_id, take_seat_data)
    return showtime_seat

@router.patch("/seats/{seat_id}/cancel", response_model=ShowtimeSeat, tags=['Showtime Seats'])
def cancel_seat(
    take_seat_data: dict,
    seat_id: int,
    usecase
):
    showtime_seat = usecase.execute(seat_id, take_seat_data)
    return showtime_seat

