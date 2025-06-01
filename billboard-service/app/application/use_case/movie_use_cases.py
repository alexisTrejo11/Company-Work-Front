from app.core.entities.movie import Movie
from app.application.interfaces import MovieRepository

class MovieGetByIdUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    async def execute(self, id: int) -> Movie:
        movie = await self.movie_repository.get_by_id(id)
        if not movie:
            raise Exception("Movie Not Found")
        
        return movie