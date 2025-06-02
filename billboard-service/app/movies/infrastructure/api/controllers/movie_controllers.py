from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ....application.use_case.movie_use_cases import (
    GetMovieByIdUseCase, GetMoviesInExhitionUseCase, 
    CreateMovieUseCase, DeleteMovieUseCase
)
from ....infrastructure.dependencies import (
    get_movie_by_id_use_case, get_active_movies_use_case,
    create_movie_use_case, delete_movie_use_case,
)
from ....core.entities.movie import Movie

router = APIRouter(prefix="/v1/api/movies")

@router.get("/{movie_id}", response_model=Movie)
async def get_movie_by_id(
    movie_id: int,
    use_case: Annotated[GetMovieByIdUseCase, Depends(get_movie_by_id_use_case)]
):
    try:
        movie = await use_case.execute(movie_id)
        return movie
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/active/", response_model=list[Movie])
async def get_movies_in_exhibition(
    use_case: Annotated[GetMoviesInExhitionUseCase, Depends(get_active_movies_use_case)]
):
    try:
        movies = await use_case.execute()
        return movies
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movies(
    movie: Movie,
    use_case: Annotated[CreateMovieUseCase, Depends(create_movie_use_case)]
):
    try:
        created_movie = await use_case.execute(movie)
        return created_movie
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
async def create_movies(
    movie: Movie,
    use_case: Annotated[CreateMovieUseCase, Depends(create_movie_use_case)]
):
    try:
        created_movie = await use_case.execute(movie)
        return created_movie
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: int,
    use_case: Annotated[DeleteMovieUseCase, Depends(delete_movie_use_case)]
):
    try:
        await use_case.execute(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))