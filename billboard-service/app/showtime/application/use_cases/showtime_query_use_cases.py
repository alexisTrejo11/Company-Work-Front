from typing import Optional, List, Dict
from ...core.entities.show_time import Showtime
from ..repositories.show_time_repository import ShowTimeRepository

class GetShowtimeByIdUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Optional[Showtime]:
        return await self.repository.get_by_id(showtime_id)


class ListShowtimesByMovieUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, filters: Dict = None, page_params: Dict = None) -> List[Showtime]:
        page_params = page_params or {'offset': 0, 'limit': 100}
        showtimes = await self.repository.get_all(page_params)
        
        if filters:
            showtimes = [s for s in showtimes if self._matches_filters(s, filters)]
        
        return showtimes


class ListShowtimesByMovieUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    # TODO: Verify Movie
    async def execute(self, movie_id: int) -> List[Showtime]:
        showtimes = self.repository.list_incoming_by_movie(movie_id) 
        return showtimes
        

class ListShowtimesByMovieUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    # TODO: Verify Cinema
    async def execute(self, cinema_id: int) -> List[Showtime]:
        showtimes = self.repository.list_incoming_by_cinema(cinema_id) 
        return showtimes
        

class ListShowtimesUseCase:
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
    