from datetime import timedelta
from ...core.entities.show_time import Showtime
from ..repositories.show_time_repository import ShowTimeRepository
from ..service.showtime_validator_service import ShowtimeValidationService
from app.shared.exceptions import NotFoundException

class ScheduleShowtimeUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, validation_service: ShowtimeValidationService):
        self.showtime_repo = showtime_repo
        self.validation_service = validation_service
    
    async def execute(self, proposed_showtime: Showtime, include_post_credits_scene: bool = False) -> Showtime:
        await self._validate_creation(proposed_showtime, include_post_credits_scene)
        
        return await self.showtime_repo.save(proposed_showtime)

    async def _validate_creation(self, proposed_showtime: Showtime, include_post_credits_scene: bool):
        proposed_showtime.validate_business_logic()
        await self.validation_service.validate_no_overlap(proposed_showtime, include_post_credits_scene)


class UpdateShowtimeUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, validation_service: ShowtimeValidationService):
        self.showtime_repo = showtime_repo
        self.validation_service = validation_service

    async def execute(self, showtime_id: int, new_data: Showtime, include_post_credits_scene: bool = False) -> Showtime:
        showtime = await self.showtime_repo.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)
        
        showtime.update(new_data)
        self._validate_update(showtime, include_post_credits_scene)

        return await self.repository.save(showtime)

    async def _validate_update(self, proposed_showtime: Showtime, include_post_credits_scene: bool):
        proposed_showtime.validate_business_logic()
        await self.validation_service.validate_no_overlap(proposed_showtime, include_post_credits_scene)


#TODO: Validate Delete
class DeleteShowtimeUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> None:
        showtime = await self.repository.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException(f"Showtime", showtime_id)
        
        await self.repository.delete(showtime_id)