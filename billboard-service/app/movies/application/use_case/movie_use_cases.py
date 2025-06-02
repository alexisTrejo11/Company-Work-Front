from ...core.entities.movie import Movie
from ...application.repositories.interfaces import MovieRepository
from typing import List


class GetMovieByIdUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository


   async def execute(self, id: int) -> Movie:
       movie = await self.movie_repository.get_by_id(id)
       if not movie:
           raise Exception("Movie Not Found")
      
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
  

class DeleteMovieUseCase:
   def __init__(self, movie_repository: MovieRepository):
       self.movie_repository = movie_repository

   async def execute(self, id: int) -> List[Movie]:
       movie = await self.movie_repository.get_by_id(id)
       if not movie:
           raise ValueError("Movie Not Found")


       await self.movie_repository.delete(movie)
