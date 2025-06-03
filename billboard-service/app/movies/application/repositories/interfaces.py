from datetime import datetime
from typing import List
from abc import ABC, abstractmethod
from ...core.entities.movie import Movie
from app.shared.repository.common_repository import CommonRepository


class MovieRepository(CommonRepository[Movie], ABC):
    """
    Specific repository interface for Movie entities.
    Inherits common CRUD methods for Movie.
    """
    # @abstractmethod
    # async def find_movies_by_genre(self, genre: str) -> List[Movie]:
    #     pass
    pass
