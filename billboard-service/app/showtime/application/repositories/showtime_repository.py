from typing import List, Dict
from datetime import datetime
from abc import ABC, abstractmethod
from app.shared.repository.common_repository import CommonRepository
from app.showtime.domain.entities.showtime import Showtime

class ShowTimeRepository(CommonRepository[Showtime]):
    @abstractmethod
    def get_incoming_by_cinema(self, cinema_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def get_incoming_by_movie(self, movie_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def get_incoming_movie_showtimes(self, movie_id: int = None, cinema_id: int = None) -> Dict[int, Showtime]:
        """
        DICT --> {key: movie_id: value: [...showtime]}
        """
        pass

    @abstractmethod
    def get_by_theater_and_date_range(
        theater_id:int, 
        start_time_to_check: datetime, 
        end_time_to_check: datetime, 
        exclude_showtime_id:int =None
    ) -> List[Showtime]:
        pass
