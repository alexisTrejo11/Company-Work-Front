from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db
from ...infrastructure.persistence.repositories.sql_alchemist_theater_repository import (
    SQLAlchemyTheaterRepository
)
from ...application.use_cases.theather_use_cases import (
    GetTheaterByIdUseCase,
    GetTheatersByCinemaUseCase,
    ListTheatersUseCase,
    CreateTheaterUseCase,
    UpdateTheaterUseCase,
    DeleteTheaterUseCase
)

async def get_theater_by_id_use_case(db: AsyncSession = Depends(get_db)) -> GetTheaterByIdUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return GetTheaterByIdUseCase(repo)

async def create_theater_use_case(db: AsyncSession = Depends(get_db)) -> CreateTheaterUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return CreateTheaterUseCase(repo)

async def get_theaters_by_cinema_use_case(db: AsyncSession = Depends(get_db)) -> GetTheatersByCinemaUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return GetTheatersByCinemaUseCase(repo)

async def list_theaters_use_case(db: AsyncSession = Depends(get_db)) -> ListTheatersUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return ListTheatersUseCase(repo)

async def update_theater_use_case(db: AsyncSession = Depends(get_db)) -> UpdateTheaterUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return UpdateTheaterUseCase(repo)

async def delete_theater_use_case(db: AsyncSession = Depends(get_db)) -> DeleteTheaterUseCase:
    repo = SQLAlchemyTheaterRepository(db)
    return DeleteTheaterUseCase(repo)
