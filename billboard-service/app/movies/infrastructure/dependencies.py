from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.persistence.repositories.sql_alchemist_movie_repository import SQLAlchemyMovieRepository
from ..application.use_case.movie_use_cases import GetMovieByIdUseCase, GetMoviesInExhitionUseCase, CreateMovieUseCase, DeleteMovieUseCase
from app.config.postgres_config import get_db

async def get_movie_by_id_use_case(
    db: AsyncSession = Depends(get_db)
) -> GetMovieByIdUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return GetMovieByIdUseCase(repo)

async def get_active_movies_use_case(
    db: AsyncSession = Depends(get_db)
) -> GetMoviesInExhitionUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return GetMoviesInExhitionUseCase(repo)

async def create_movie_use_case(
    db: AsyncSession = Depends(get_db)
) -> CreateMovieUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return CreateMovieUseCase(repo)

async def delete_movie_use_case(
    db: AsyncSession = Depends(get_db)
) -> DeleteMovieUseCase:
    repo = SQLAlchemyMovieRepository(db)
    return DeleteMovieUseCase(repo)