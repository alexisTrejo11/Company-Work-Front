from typing import List, Optional
from abc import ABC, abstractmethod
from shared.repository.common_repository import CommonRepository
from ...core.entities.show_time import Showtime

class ShowTimeRepository(ABC, CommonRepository[Showtime]):
    @abstractmethod
    def list_incoming_by_cinema(cinema_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def list_incoming_by_movie(movie_id:int) -> List[Showtime]:
        pass
