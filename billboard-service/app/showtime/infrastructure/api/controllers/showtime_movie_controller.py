from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends
from ....core.entities.showtime import Showtime

router = APIRouter(prefix="/api/v1/movie-showtimes", tags=["movie-showtimes"])

@router.get("/incoming/movie/{movie_id}", response_model=List[Showtime])
async def get_incoming_showtimes_by_movie(
    movie_id: int,
    use_case
):
    showtimes = await use_case.execute(movie_id)
    
    return showtimes

@router.get("/cinema/{cinema_id}", response_model=List[Showtime])
async def get_incoming_showtimes_by_cinema(
    cinema_id: int,
    use_case
):
    showtimes = await use_case.execute(cinema_id)
    
    return showtimes

