from typing import Optional, List, Dict
from ...core.entities.show_time import Showtime
from ..repositories.show_time_repository import ShowTimeRepository
from app.movies.application.repositories.interfaces import MovieRepository
from app.cinema.application.repository.cinema_repository import CinemaRepository
from app.shared.exceptions import NotFoundException


class GetShowtimeByIdUseCase:
    def __init__(self, repository: ShowTimeRepository):
        self.repository = repository

    async def execute(self, showtime_id: int) -> Optional[Showtime]:
        return await self.repository.get_by_id(showtime_id)


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
    

class GetIncomingShowtimesByMovieUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, movie_repo: MovieRepository):
        self.showtime_repo = showtime_repo
        self.movie_repo = movie_repo

    async def execute(self, movie_id: int) -> List[Showtime]:
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise NotFoundException(f"Movie", movie_id)

        return self.showtime_repo.list_incoming_by_movie(movie_id) 


class GetIncomingShowtimesByCinemaUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, cinema_repo: CinemaRepository):
        self.showtime_repo = showtime_repo
        self.cinema_repo = cinema_repo

    async def execute(self, cinema_id: int) -> List[Showtime]:
        cinema = self.cinema_repo.get_by_id(cinema_id)
        if not cinema:
            raise NotFoundException(f"Cinema", cinema_id)

        return self.repository.list_incoming_by_cinema(cinema_id) 
