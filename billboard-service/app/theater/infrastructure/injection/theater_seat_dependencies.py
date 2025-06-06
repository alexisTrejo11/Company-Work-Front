from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db
from ..persistence.repositories.sqlalchemist_theater_seats_repository import SqlAlchemistTheaterSeatRepository
from ..persistence.repositories.sqlalchemist_theater_repository import  SQLAlchemyTheaterRepository
from ...application.use_cases.seats_use_cases import GetTheaterSeatByIdUseCase, GetSeatsByTheaterUseCase, CreateTheaterSeatUseCase, UpdateTheaterSeatUseCase, DeleteTheaterSeatUseCase
from ...application.service.seat_validation_service import SeatValidationService

async def get_theater_seat_by_id_use_case(db: AsyncSession = Depends(get_db)) -> GetTheaterSeatByIdUseCase:
    """
    Dependency for GetTheaterSeatByIdUseCase.
    Provides an instance of the use case with an injected repository.
    """
    repository = SqlAlchemistTheaterSeatRepository(db)
    
    return GetTheaterSeatByIdUseCase(repository)

async def get_seats_by_theater_use_case(db: AsyncSession = Depends(get_db)) -> GetSeatsByTheaterUseCase:
    """
    Dependency for GetSeatsByTheaterUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SqlAlchemistTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)
    
    return GetSeatsByTheaterUseCase(seat_repository=seat_repository, theater_repository=theather_repository)

async def create_theater_seat_use_case(db: AsyncSession = Depends(get_db)) -> CreateTheaterSeatUseCase:
    """
    Dependency for SaveTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SqlAlchemistTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)
    validationService = SeatValidationService(seat_repository=seat_repository, theater_repository=theather_repository)
    
    return CreateTheaterSeatUseCase(seat_repository=seat_repository, validation_service=validationService)

async def update_theater_seat_use_case(db: AsyncSession = Depends(get_db)) -> UpdateTheaterSeatUseCase:
    """
    Dependency for SaveTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    seat_repository = SqlAlchemistTheaterSeatRepository(db)
    theather_repository = SQLAlchemyTheaterRepository(db)
    validationService = SeatValidationService(seat_repository=seat_repository, theater_repository=theather_repository)
    
    return UpdateTheaterSeatUseCase(seat_repository=seat_repository, validation_service=validationService)

async def delete_theater_seat_use_case(db: AsyncSession = Depends(get_db)) -> DeleteTheaterSeatUseCase:
    """
    Dependency for DeleteTheaterSeatUseCase.
    Provides an instance of the use case with an injected repository.
    """
    repository = SqlAlchemistTheaterSeatRepository(db)
    
    return DeleteTheaterSeatUseCase(repository)