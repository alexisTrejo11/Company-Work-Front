from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..persistence.repository.sql_alchemist_cinema_repository import SQLAlchemyCinemaRepository
from ...application.use_case.cinema_use_cases import GetCinemaByIdUseCase, GetActiveCinemasUseCase, SearchCinemasUseCase, CreateCinemaUseCase, UpdateCinemaUseCase, DeleteCinemaUseCase
from app.config.postgres_config import get_db

# Query
async def get_cinema_by_id_use_case(db: AsyncSession = Depends(get_db)) -> GetCinemaByIdUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return GetCinemaByIdUseCase(repo)

async def get_active_cinemas_use_case(db: AsyncSession = Depends(get_db)) -> GetActiveCinemasUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return GetActiveCinemasUseCase(repo)

async def search_cinemas_use_case(db: AsyncSession = Depends(get_db)) -> SearchCinemasUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return SearchCinemasUseCase(repo)


# Command
async def create_cinema_use_case(db: AsyncSession = Depends(get_db)) -> CreateCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return CreateCinemaUseCase(repo)

async def update_cinema_use_case(db: AsyncSession = Depends(get_db)) -> UpdateCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return UpdateCinemaUseCase(repo)

async def delete_cinema_use_case(db: AsyncSession = Depends(get_db)) -> DeleteCinemaUseCase:
    repo = SQLAlchemyCinemaRepository(db)
    return DeleteCinemaUseCase(repo)