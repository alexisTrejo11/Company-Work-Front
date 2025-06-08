from typing import List, Dict
from ..repository.cinema_repository import CinemaRepository 
from ...core.entities.cinema import Cinema
from ...core.exceptions import CinemaNotFound

class GetCinemaByIdUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    async def execute(self, cinema_id: int) -> Cinema:
        cinema = await self.repository.get_by_id(cinema_id)
        if not cinema:
            raise CinemaNotFound("Cinema", cinema_id)
        return cinema


class SearchCinemasUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    async def execute(self, page_params: Dict[str, int], filter_params: Dict[str, any]) -> List[Cinema]:
        return await self.repository.search(page_params, filter_params)

class GetActiveCinemasUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    def execute(self) -> List[Cinema]:
        return self.repository.get_active_cinemas()


class CreateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    def execute(self, new_cinema: Cinema) -> Cinema:
        return self.repository.save(new_cinema)


class UpdateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    async def execute(self, cinema_id: int, cinema_updated: Cinema) -> Cinema:
        cinema = await self.repository.get_by_id(cinema_id)
        if not cinema:
            raise CinemaNotFound(f"Cinema", cinema_id)
        
        cinema_updated.id = cinema_id
        return await self.repository.save(cinema_updated)

class DeleteCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    async def execute(self, cinema_id: int) -> None:
        cinema = await self.repository.get_by_id(cinema_id)
        if not cinema:
            raise CinemaNotFound(f"Cinema", cinema_id)
        
        await self.repository.delete(cinema)
