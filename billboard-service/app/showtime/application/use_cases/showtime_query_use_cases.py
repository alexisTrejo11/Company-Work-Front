from typing import Optional, List, Dict
from ...core.entities.showtime import Showtime
from ..repositories.showtime_repository import ShowTimeRepository
from app.movies.application.repositories.interfaces import MovieRepository
from app.cinema.application.repository.cinema_repository import CinemaRepository
from app.shared.exceptions import NotFoundException

class GetShowtimeByIdUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Optional[Showtime]:
        showtime = await self.repository.get_by_id(showtime_id)
        if not showtime:
            raise NotFoundException("Showtime", showtime_id)

        return showtime
    

class GetShowtimesUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, filters: Dict = None, page_params: Dict = None) -> List[Showtime]:
        page_params = page_params or {'offset': 0, 'limit': 100}
        showtimes = await self.repository.get_all(page_params)
        
        if filters:
            showtimes = [s for s in showtimes if self._matches_filters(s, filters)]
        
        return showtimes

    def _matches_filters(self, showtime: Showtime, filters: Dict) -> bool:
        if 'movie_id' in filters and showtime.movie_id != filters['movie_id']:
            return False
        if 'theater_id' in filters and showtime.theater_id != filters['theater_id']:
            return False
        if 'is_active' in filters and showtime.is_active != filters['is_active']:
            return False
        return True
    
