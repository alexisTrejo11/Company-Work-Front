from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends
from ....core.entities.showtime import Showtime
from ....application.use_cases.showtime_query_use_cases import GetShowtimeByIdUseCase, GetShowtimesUseCase, GetIncomingShowtimesByMovieUseCase, GetIncomingShowtimesByCinemaUseCase
from ...injection.depdencies import get_incoming_showtime_by_cinema_use_case, get_incoming_showtime_by_movie_use_case

router = APIRouter(prefix="/api/v1/movie-showtimes", tags=["showtimes"])

@router.get("/incoming/movie/{movie_id}", response_model=Showtime)
async def get_incoming_showtimes_by_movie(
    movie_id: int,
    use_case: GetIncomingShowtimesByMovieUseCase = Depends(get_incoming_showtime_by_movie_use_case)
):
    showtimes = await use_case.execute(movie_id)
    if not showtimes:
        return []
    
    return showtimes

@router.get("/cinema/{cinema_id}", response_model=Showtime)
async def get_incoming_showtimes_by_cinema(
    cinema_id: int,
    use_case: GetIncomingShowtimesByCinemaUseCase = Depends(get_incoming_showtime_by_cinema_use_case)
):
    showtimes = await use_case.execute(cinema_id)
    if not showtimes:
        return []
    
    return showtimes

