from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass
from app.showtime.domain.entities.showtime import Showtime

@dataclass
class MovieShowtime:
    """
    Class to Represent a Showtime with Cinema with required field to show it on 
    billboard catalog
    """
    movie_id: int
    title: str
    sinopsis: str
    poster_url: str
    rating: str
    minute_duration: int
    showtimes: List['ShowtimeDetail']
 
@dataclass
class ShowtimeDetail(BaseModel):
    showtime_id: int
    type: str # IMAX
    start_time: str
    language: str
    screen: str # Theater ID with Theather {id} 
    total_seats: int
    avaailable_seats: int


class MovieShowtimesFilters(BaseModel):
    cinema_id_list: Optional[List[int]] = None, 
    movie_id: Optional[int] = None,
    incoming: bool = True,



@dataclass
class ShowtimesByMovie:
    movie_id: int
    showtimes: List['Showtime']
