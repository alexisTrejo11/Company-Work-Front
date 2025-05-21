from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic, Dict
from datetime import datetime

from app.core.entities.cinema import Cinema
from app.core.entities.theater import Theater
from app.core.entities.movie import Movie
from app.core.entities.show_time import Showtime

T = TypeVar('T')

class CommonRepository(ABC, Generic[T]):
    """
    Generic abstract base class for common CRUD repository operations.
    T represents the specific Domain Entity type (e.g., Cinema, Movie).
    """

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Retrieves a single entity by its ID.
        """
        pass

    @abstractmethod
    async def get_all(self, page_params: Dict[str, int]) -> List[T]:
        """
        Retrieves a list of entities with pagination parameters.
        page_params should contain 'offset' and 'limit'.
        """
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """
        Saves a new entity or updates an existing one.
        If the entity has no ID, it's typically considered new.
        Returns the saved/updated entity, often with its assigned ID.
        """
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> None:
        """
        Deletes an entity by its ID.
        """
        pass


class CinemaRepository(CommonRepository[Cinema], ABC):
    """
    Specific repository interface for Cinema entities.
    Inherits common CRUD methods for Cinema.
    """
    @abstractmethod
    async def get_cinemas_by_tax_number(self, tax_number: str) -> Optional[Cinema]:
        pass


class TheaterRepository(CommonRepository[Theater], ABC):
    """
    Specific repository interface for Theater entities.
    Inherits common CRUD methods for Theater.
    """
    @abstractmethod
    async def get_theaters_by_cinema(self, cinema_id: int) -> List[Theater]:
        pass


class MovieRepository(CommonRepository[Movie], ABC):
    """
    Specific repository interface for Movie entities.
    Inherits common CRUD methods for Movie.
    """
    # @abstractmethod
    # async def find_movies_by_genre(self, genre: str) -> List[Movie]:
    #     pass
    pass


class ShowtimeRepository(CommonRepository[Showtime], ABC):
    """
    Specific repository interface for Showtime entities.
    Inherits common CRUD methods for Showtime.
    """
    @abstractmethod
    async def get_showtimes_for_movie_and_date(self, movie_id: int, date: datetime) -> List[Showtime]:
        pass