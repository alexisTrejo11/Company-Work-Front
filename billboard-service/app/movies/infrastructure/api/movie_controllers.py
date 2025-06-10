from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.movies.domain.entities import Movie
from app.movies.application.use_cases import GetMovieByIdUseCase, GetMoviesInExhitionUseCase, UpdateMovieUseCase, CreateMovieUseCase, DeleteMovieUseCase
from .dependencies import get_movie_by_id_use_case, get_active_movies_use_case, create_movie_use_case, update_movie_use_case, delete_movie_use_case

router = APIRouter(prefix="/api/v1/movies")

@router.get("/{movie_id}", response_model=Movie)
async def get_movie_by_id(
    movie_id: int,
    use_case: Annotated[GetMovieByIdUseCase, Depends(get_movie_by_id_use_case)]
):
    movie = await use_case.execute(movie_id)
    return movie

    
@router.get("/active/", response_model=list[Movie])
async def get_movies_in_exhibition(
    use_case: Annotated[GetMoviesInExhitionUseCase, Depends(get_active_movies_use_case)]
):
    movies = await use_case.execute()
    return movies


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movies(
    movie: Movie,
    use_case: Annotated[CreateMovieUseCase, Depends(create_movie_use_case)]
):
    created_movie = await use_case.execute(movie)
    return created_movie


@router.put("/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
async def update_movie(
    movie_id: int,
    movie: Movie,
    use_case: Annotated[UpdateMovieUseCase, Depends(update_movie_use_case)]
):

    created_movie = await use_case.execute(movie_id, movie)
    return created_movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int,
    use_case: Annotated[DeleteMovieUseCase, Depends(delete_movie_use_case)]
):
    await use_case.execute(movie_id)
