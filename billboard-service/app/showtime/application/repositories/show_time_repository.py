from typing import List
from abc import ABC, abstractmethod
from app.shared.repository.common_repository import CommonRepository
from ...core.entities.show_time import Showtime
from datetime import datetime

class ShowTimeRepository(CommonRepository[Showtime]):
    @abstractmethod
    def get_incoming_by_cinema(cinema_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def get_incoming_by_movie(movie_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def get_by_theater_and_date_range(
        theater_id:int, 
        start_time_to_check: datetime, 
        end_time_to_check: datetime, 
        exclude_showtime_id:int =None
    ) -> List[Showtime]:
        pass
