from typing import List
from ..repository.cinema_repository import CinemaRepository 
from ...core.entities.cinema import Cinema

class GetCinemaByIdUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    def execute(self, cinema_id: int) -> Cinema:
        cinema = self.repository.get_by_id(cinema_id)
        if not cinema:
            raise ValueError("Cinema Not Found")
        
        return cinema


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


class DeleteCinemaUseCase:
    def __init__(self, repository: CinemaRepository):
        self.repository = repository
    
    async def execute(self, cinema_id: int) -> None:
        cinema = await self.repository.get_by_id(cinema_id)
        if not cinema:
            raise ValueError("Cinema Not Found")
        
        await self.repository.delete(cinema)
