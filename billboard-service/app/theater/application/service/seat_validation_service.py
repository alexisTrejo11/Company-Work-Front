from app.shared.exceptions import NotFoundException, ValidationException
from ...application.dtos.seat_dtos import TheaterSeatCreate, TheaterSeatUpdate
from ...application.repositories.theater_seat_repository import TheaterSeatRepository
from ...application.repositories.theater_repository import TheaterRepository

class SeatValidationService:
    def __init__(self, seat_repository: TheaterSeatRepository, theater_repository: TheaterRepository):
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    async def validate_seat_create(self, seat_data: TheaterSeatCreate):
            await self.validate_theater(seat_data.theater_id)
            await self.validate_not_duplicated_seat(seat_data.theater_id, seat_data.seat_row, seat_data.seat_number)

    async def validate_seat_update(self, seat_data: TheaterSeatUpdate):
        await self.validate_theater(seat_data.theater_id)
        await self.validate_not_duplicated_seat(seat_data.theater_id, seat_data.seat_row, seat_data.seat_number)

    async def validate_theater(self, theater_id: int=None) -> None:
            if not theater_id:
                return
            
            theater = await self.theater_repository.get_by_id(theater_id)
            if not theater:
                raise NotFoundException("Theater", theater_id)
            
    async def validate_not_duplicated_seat(self, theater_id, seat_row, seat_number):
            is_seat_duplicated =  self.seat_repository.exist_by_theater_and_seat_values(
                theater_id=theater_id, 
                seat_row=seat_row, 
                seat_number= seat_number
            )
            if is_seat_duplicated:
                raise ValidationException(
                    field="Seat row-number",
                    reason="Seat row-number already exists in this theater"
                )
