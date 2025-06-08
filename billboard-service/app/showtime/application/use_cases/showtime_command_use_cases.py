from datetime import timedelta
from app.shared.exceptions import NotFoundException
from ...application.mappers.showtime_mappers import ShowtimeMappers
from ...application.dtos.showtime_dtos import ShowtimeCreate, ShowtimeUpdate
from ...core.entities.showtime import Showtime
from ..repositories.showtime_repository import ShowTimeRepository
from ..service.showtime_validator_service import ShowtimeValidationService as ValidationService
from ..service.showtime_seat_service import ShowTimeSeatService

class ScheduleShowtimeUseCase:
    def __init__(
            self, 
            showtime_repo: ShowTimeRepository, 
            validation_service: ValidationService, 
            seat_service : ShowTimeSeatService
        ):
        self.showtime_repo = showtime_repo
        self.validation_service = validation_service
        self.seat_service = seat_service
    
    async def execute(self, showtime_data: ShowtimeCreate, has_post_credits: bool = False) -> Showtime:
        proposed_showtime = ShowtimeMappers.from_create_dto(showtime_data)
        
        await self._validate_creation(proposed_showtime, has_post_credits)
        
        showtime_created = await self.showtime_repo.save(proposed_showtime)
        self.seat_service.create_showtimes_seats(showtime_created)

        return showtime_created

    async def _validate_creation(self, proposed_showtime: Showtime, has_post_credits: bool):
        proposed_showtime.validate_business_logic()
        await self.validation_service.validate_no_overlap(proposed_showtime, has_post_credits)
        await self.validation_service.validate_theater_seats(proposed_showtime.theater_id)


class UpdateShowtimeUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, validation_service: ValidationService):
        self.showtime_repo = showtime_repo
        self.validation_service = validation_service

    async def execute(self, showtime_id: int, update_data: ShowtimeUpdate, has_post_credits: bool = False) -> Showtime:
        existing_showtime = await self.get_showtime(showtime_id)

        showtime_upddated = ShowtimeMappers.update_with_dto(update_data, existing_showtime)
        self.validation_service.validate_insert(showtime_upddated, has_post_credits)

        return await self.repository.save(showtime_upddated)

    async def get_showtime(self, showtime_id: int) -> Showtime:
        showtime = await self.showtime_repo.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)
        

#TODO: Validate Delete
class DeleteShowtimeUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> None:
        showtime = await self.repository.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException(f"Showtime", showtime_id)
        
        await self.repository.delete(showtime_id)