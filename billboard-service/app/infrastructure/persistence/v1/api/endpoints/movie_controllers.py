
from typing import Annotated
from app.application.use_case.movie_use_cases import MovieGetByIdUseCase
from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.persistence.v1.api.depdencies import get_movie_by_id_use_case

router = APIRouter(prefix="/v1/api/movies")

@router.get("/{movie_id}")
async def read_movie_by_id(
    movie_id: int,
    movie_service: Annotated[MovieGetByIdUseCase, Depends(get_movie_by_id_use_case)]
):
    try:
        return await movie_service.execute(movie_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))