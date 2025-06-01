# app/api/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.v1.api.repositories.test_movie_repository import SQLAlchemyMovieRepository
from app.application.use_case.movie_use_cases import MovieGetByIdUseCase
from app.config.postgres_config import get_db

async def get_movie_by_id_use_case(
    db: AsyncSession = Depends(get_db)
) -> MovieGetByIdUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return MovieGetByIdUseCase(repo)