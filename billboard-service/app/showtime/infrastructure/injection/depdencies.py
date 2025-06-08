# Infrastrucutre
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db

# Module
from ...application.use_cases.showtime_command_use_cases import ScheduleShowtimeUseCase, UpdateShowtimeUseCase, DeleteShowtimeUseCase
from ...application.use_cases.showtime_query_use_cases import  GetShowtimesUseCase, GetShowtimeByIdUseCase
from ...application.service.showtime_validator_service import ShowtimeValidationService
from ..persistence.repositories.sqlalch_show_repository import SQLAlchemyShowtimeRepository
from ...application.service.showtime_seat_service import ShowTimeSeatService
from ..persistence.repositories.sqlalch_show_seat_repository import SqlAlchShowtimeSeatRepository

# External Modules
from app.cinema.infrastructure.persistence.repository.sql_alchemist_cinema_repository import SQLAlchemyCinemaRepository
from app.movies.infrastructure.persistence.repositories.sql_alchemist_movie_repository import SQLAlchemyMovieRepository
from app.theater.infrastructure.persistence.repositories.sqlalchemist_theater_seats_repository import SqlAlchemistTheaterSeatRepository

# COMMAND
async def schedule_showtime_use_case(db: AsyncSession = Depends(get_db)) -> ScheduleShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    showtime_seat_repo = SqlAlchShowtimeSeatRepository(db)
    theater_seat_repository = SqlAlchemistTheaterSeatRepository(db)

    validation_service = ShowtimeValidationService(showtime_repo, theater_seat_repository)
    showtime_seat_service = ShowTimeSeatService(theater_seat_repository, showtime_seat_repo)

    return ScheduleShowtimeUseCase(showtime_repo, validation_service, showtime_seat_service)

async def update_showtime_use_case(db: AsyncSession = Depends(get_db)) -> UpdateShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    theater_seat_repository = SqlAlchemistTheaterSeatRepository(db)

    validation_service = ShowtimeValidationService(showtime_repo, theater_seat_repository)
    return UpdateShowtimeUseCase(showtime_repo, validation_service)

async def delete_showtime_use_case(db: AsyncSession = Depends(get_db)) -> DeleteShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return DeleteShowtimeUseCase(showtime_repo)


# QUERIES
async def get_showtimes_use_case(db: AsyncSession = Depends(get_db)) -> GetShowtimesUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimesUseCase(showtime_repo)

async def get_showtime_by_id_use_case(db: AsyncSession = Depends(get_db)) -> GetShowtimeByIdUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    return GetShowtimeByIdUseCase(showtime_repo)
