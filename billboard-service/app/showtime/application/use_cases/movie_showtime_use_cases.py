from typing import List, Dict
from ..repositories.showtime_repository import ShowTimeRepository
from ..dtos.movie_showtime import MovieShowtimeDTO as MovieShowtime, ShowtimeDTO
from app.showtime.domain.entities.showtime import Showtime
from app.movies.application.repositories import MovieRepository
from app.movies.domain.entities import Movie

# TODO: Add Repository funcs and Add Cinema Region / Check ASYNC 
class GetIncomingMovieShowtimesUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, movie_repo: MovieRepository):
        self.showtime_repo = showtime_repo
        self.movie_repo = movie_repo
    
    async def execute(self, region_id: int=None, cinema_id=None, movie_id=None) -> List[MovieShowtime]:
        movies = await self.movie_repo.get_in_exhibition()
        incoming_show_times = await self.showtime_repo.get_incoming_movie_showtimes(movie_id, cinema_id)
        
        return await self._generate_movie_showtimes(movies, incoming_show_times)

    async def _generate_movie_showtimes(
        self, 
        movies: List[Movie], 
        incoming_showtimes: Dict[int, List[Showtime]]
    ) -> List[MovieShowtime]:
        movie_showtimes = []
        
        for movie in movies:
            showtimes_per_movie = incoming_showtimes.get(f'{movie.id}')
            
            showtimes_DTOs = self._generate_showtimes_dtos(showtimes_per_movie)
            movie_showtime = MovieShowtime(
                movie_id=movie.movie_id,
                title=movie.title,
                poster_url=movie.poster_url,
                minute_duration=movie.minute_duration,
                showtimes = showtimes_DTOs,
            )
            
            movie_showtimes.append(movie_showtime)

        return movie_showtimes

    def _generate_showtimes_dtos(self, showtimes: List[Showtime]) -> List[ShowtimeDTO]:
        showtimes_dtos = []
        
        for showtime in showtimes:
            dto = ShowtimeDTO(
                showtime_id=showtime.id,
                type=showtime.type,
                start_time=showtime.start_time,
                language=showtime.language,
                total_seats=showtime.total_seats,
                avaailable_seats=showtime.avaialble_seats,
            )
            showtimes_dtos.append(dto)

        return showtimes_dtos