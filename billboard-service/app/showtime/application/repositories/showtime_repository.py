from typing import Dict, List
from datetime import datetime
from abc import abstractmethod
from app.shared.repository.common_repository import CommonRepository
from app.shared.pagination import PaginationParams
from app.showtime.domain.entities.showtime import Showtime
from app.movies.application.dtos import MovieShowtimesFilters

class ShowTimeRepository(CommonRepository[Showtime]):
    @abstractmethod
    def get_incoming_by_cinema(self, cinema_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def get_incoming_by_movie(self, movie_id:int) -> List[Showtime]:
        pass

    @abstractmethod
    def list_by_filters_group_by_movie(self, showtime_filters: MovieShowtimesFilters, page_params: PaginationParams) -> Dict[int, Showtime]:
        pass

    @abstractmethod
    def get_by_theater_and_date_range(theater_id:int, start_time_to_check: datetime, end_time_to_check: datetime, exclude_showtime_id:int =None) -> List[Showtime]:
        pass
