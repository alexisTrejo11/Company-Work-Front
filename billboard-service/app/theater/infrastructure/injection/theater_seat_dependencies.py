from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db

from ..persistence.repositories.sqlalchemist_theater_seats_repository import (
    SqlAlchemistTheaterSeatRepository
)

from ..persistence.repositories.sqlalchemist_theater_repository import (
    SQLAlchemyTheaterRepository
)

from ...application.use_cases.seats_use_cases import (
    GetTheaterSeatByIdUseCase,
    GetSeatsByTheaterUseCase,
    SaveTheaterSeatUseCase,
    DeleteTheaterSeatUseCase
)

async def get_theater_seat_by_id_use_case(
    db: AsyncSession = Depends(get_db)
) -> GetTheaterSeatByIdUseCase:
    """
    Dependency for GetTheaterSeatByIdUseCase.
    Provides an instance of the use case with an injected repository.
    """
    repository = SqlAlchemistTheaterSeatRepository(db)
    return GetTheaterSeatByIdUseCase(repository)

async def get_seats_by_theater_use_case(
    db: AsyncSession = Depends(get_db)
) -> GetSeatsByTheaterUseCase:
    """
    Dependency for GetSeatsByTheaterUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SqlAlchemistTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)
    return GetSeatsByTheaterUseCase(seat_repository=seat_repository, theater_repository=theather_repository)

async def save_theater_seat_use_case(
    db: AsyncSession = Depends(get_db)
) -> SaveTheaterSeatUseCase:
    """
    Dependency for SaveTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SqlAlchemistTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)

    return SaveTheaterSeatUseCase(seat_repository=seat_repository, theater_repository=theather_repository)

async def delete_theater_seat_use_case(
    db: AsyncSession = Depends(get_db)
) -> DeleteTheaterSeatUseCase:
    """
    Dependency for DeleteTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    repository = SqlAlchemistTheaterSeatRepository(db)
    return DeleteTheaterSeatUseCase(repository)