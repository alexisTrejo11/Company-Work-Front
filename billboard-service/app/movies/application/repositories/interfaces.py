from datetime import datetime
from typing import List
from abc import ABC, abstractmethod
from ...core.entities.theater import Theater
from ...core.entities.movie import Movie
from ...core.entities.show_time import Showtime
from app.shared.repository.common_repository import CommonRepository

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