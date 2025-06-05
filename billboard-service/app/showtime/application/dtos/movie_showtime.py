from pydantic import BaseModel
from typing import List

class MovieShowtimeDTO(BaseModel):
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
    showtimes: List['ShowtimeDTO']
 
class ShowtimeDTO(BaseModel):
    showtime_id: int
    type: str # IMAX
    start_time: str
    language: str
    screen: str # Theater ID with Theather {id} 
    total_seats: int
    avaailable_seats: int


