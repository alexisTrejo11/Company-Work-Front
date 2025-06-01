from app.application.interfaces import MovieRepository
from typing import Optional, Dict, List
from app.core.entities.movie import Movie
from ..models.models import MovieModel
from sqlalchemy.ext.asyncio import AsyncSession
from .....mappers.movie_mappers import MovieMapper


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self,  session: AsyncSession):
        self.session = session

    async def get_by_id(self, movie_id: int) -> Optional[Movie]:
        model = await self.session.get(MovieModel, movie_id)
        if model:
            return MovieMapper.to_entity(model)
        return None

    async def get_all(self, page_params: Dict[str, int]) -> List[Movie]:
        """
        Retrieves a list of entities with pagination parameters.
        page_params should contain 'offset' and 'limit'.
        """
        pass

    async def save(self, entity: Movie) -> Movie:
        """
        Saves a new entity or updates an existing one.
        If the entity has no ID, it's typically considered new.
        Returns the saved/updated entity, often with its assigned ID.
        """
        pass

    async def delete(self, entity_id: int) -> None:
        """
        Deletes an entity by its ID.
        """
        pass
