from typing import Optional, List, Dict
from ...core.entities.show_time import Showtime
from ..repositories.show_time_repository import ShowTimeRepository

#TODO: Check Schedule Not Conflict
class CreateShowtimeUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository):
        self.showtime_repo = showtime_repo
    
    async def execute(self, showtime: Showtime) -> Showtime:
        showtime.validate_business_logic()
        return await self.showtime_repo.create(showtime)

class UpdateShowtimeUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int, new_data: Showtime) -> Showtime:
        showtime = await self.repository.get_by_id(showtime_id)
        if not showtime:
            raise ValueError("Showtime not found")
        
        showtime.update(new_data)
        showtime.validate_business_logic()

        return await self.repository.save(showtime)

#TODO: Validate Delete
class DeleteShowtimeUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> None:
        await self.repository.delete(showtime_id)