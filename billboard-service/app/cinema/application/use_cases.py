from typing import List, Dict
from app.cinema.domain.entities import Cinema
from app.cinema.application.dtos.cinema_insert import CinemaCreate, CinemaUpdate
from app.cinema.domain.exceptions import CinemaNotFound
from .repository import CinemaRepository 
from .mappers import CinemaMapper

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
    
    def execute(self, create_data: CinemaCreate) -> Cinema:
        new_cinema = CinemaMapper.from_create_dto(create_data)

        return self.repository.save(new_cinema)


class UpdateCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    async def execute(self, cinema_id: int, update_data: CinemaUpdate) -> Cinema:
        existing_cinema = await self.repository.get_by_id(cinema_id)
        if not existing_cinema:
            raise CinemaNotFound(f"Cinema", cinema_id)
        
        cinema_updated = CinemaMapper.update_cinema_from_dto(existing_cinema, update_data)
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
