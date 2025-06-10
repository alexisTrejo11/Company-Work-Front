from typing import List
from app.shared.pagination import PaginationParams
from app.movies.domain.entities import Movie
from app.movies.application.repositories import MovieRepository
from app.movies.domain.entities import Movie
from app.showtime.application.repositories.showtime_repository import ShowTimeRepository
from .dtos import MovieShowtime, MovieShowtimesFilters
from .repositories import MovieRepository
from .services import MovieShowtimeService
from app.shared.exceptions import NotFoundException

class GetMovieByIdUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository

   async def execute(self, id: int) -> Movie:
       movie = await self.movie_repository.get_by_id(id)
       if not movie:
           raise NotFoundException("Movie", id)
      
       return movie
  
class GetMoviesInExhitionUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository

   async def execute(self) -> List[Movie]:
       movies = await self.movie_repository.get_active_movies()
       return movies


class CreateMovieUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository

   async def execute(self, new_movie: Movie) -> List[Movie]:
       movies = await self.movie_repository.save(new_movie)
       return movies
   
class UpdateMovieUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository

   async def execute(self, movie_id: int, movie_updated: Movie) -> List[Movie]:
        movie = await self.movie_repository.get_by_id(movie_id)
        if not movie:
           raise NotFoundException("Movie", movie_id)
        
        movie_updated.id = movie_id
        movies = await self.movie_repository.save(movie_updated)
        return movies
  

class DeleteMovieUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository

   async def execute(self, id: int) -> List[Movie]:
       movie = await self.movie_repository.get_by_id(id)
       if not movie:
           raise NotFoundException("Movie", id)

       await self.movie_repository.delete(movie)


class GetMovieShowtimesUseCase:
    def __init__(self, showtime_repo: ShowTimeRepository, movie_repo: MovieRepository):
        self.showtime_repo = showtime_repo
        self.movie_repo = movie_repo
    
    async def execute(self, filters: MovieShowtimesFilters, page_data: PaginationParams) -> List[MovieShowtime]:
        movies = await self.movie_repo.get_in_exhibition()
        if not movies:
            return []

        incoming_show_times = await self.showtime_repo.list_by_filters_group_by_movie(filters, page_data)

        movie_showtimes = MovieShowtimeService.generate_movie_showtimes(movies, incoming_show_times)
        return movie_showtimes
