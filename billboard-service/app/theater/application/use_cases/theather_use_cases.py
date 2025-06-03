from typing import Optional, Dict, List
from ...core.entities.theater import Theater
from ..repositories.theater_repository import TheaterRepository

class GetTheaterByIdUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, theater_id: int) -> Optional[Theater]:
        return await self.repository.get_by_id(theater_id)
    
    
class GetTheatersByCinemaUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, cinema_id: int) -> List[Theater]:
        return await self.repository.get_by_cinema(cinema_id)


class ListTheatersUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, page_params: Dict = None) -> List[Theater]:
        page_params = page_params or {'offset': 0, 'limit': 100}
        theaters = await self.repository.get_all(page_params)
        
        return theaters
    

class CreateTheaterUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, theater: Theater) -> Theater:
        theater.validate_buissness_rules()
        return await self.repository.save(theater)
    

class UpdateTheaterUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, theater_id: int, update_data: Theater) -> Theater:
        theater = await self.repository.get_by_id(theater_id)
        if not theater:
            raise ValueError("Theater not found")
        
        theater.update(update_data) 
        theater.validate_buissness_rules()

        return await self.repository.save(theater)


class DeleteTheaterUseCase:
    def __init__(self, repository: TheaterRepository):
        self.repository = repository

    async def execute(self, theater_id: int) -> None:
        theater = await self.repository.get_by_id(theater_id)
        if not theater:
            raise ValueError("Theater not found")
        
        await self.repository.delete(theater_id)