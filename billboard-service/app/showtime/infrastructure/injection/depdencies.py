from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.postgres_config import get_db
from ...application.use_cases.showtime_command_use_cases import (
    ScheduleShowtimeUseCase, UpdateShowtimeUseCase, DeleteShowtimeUseCase
)
from ...application.use_cases.showtime_query_use_cases import (
    GetShowtimesUseCase, GetShowtimeByIdUseCase,
    GetIncomingShowtimesByCinemaUseCase, GetIncomingShowtimesByMovieUseCase
)
from ...application.service.showtime_validator_service import ShowtimeValidationService
from ..persistence.repositories.sql_alchemist_showtime_repository import SQLAlchemyShowtimeRepository
from app.cinema.infrastructure.persistence.repository.sql_alchemist_cinema_repository import SQLAlchemyCinemaRepository
from app.movies.infrastructure.persistence.repositories.sql_alchemist_movie_repository import SQLAlchemyMovieRepository

# COMMAND
async def schedule_showtime_use_case(db: AsyncSession = Depends(get_db)) -> ScheduleShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    validation_service = ShowtimeValidationService(showtime_repo)
    return ScheduleShowtimeUseCase(showtime_repo, validation_service)

async def update_showtime_use_case(db: AsyncSession = Depends(get_db)) -> UpdateShowtimeUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    validation_service = ShowtimeValidationService(showtime_repo)
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

async def get_incoming_showtime_by_cinema_use_case(db: AsyncSession = Depends(get_db)) -> GetIncomingShowtimesByCinemaUseCase:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    cinema_repo = SQLAlchemyCinemaRepository(db)
    return GetIncomingShowtimesByCinemaUseCase(showtime_repo, cinema_repo)

async def get_incoming_showtime_by_movie_use_case(db: AsyncSession = Depends(get_db)) -> SQLAlchemyMovieRepository:
    showtime_repo = SQLAlchemyShowtimeRepository(db)
    cinema_repo = SQLAlchemyCinemaRepository(db)
    return SQLAlchemyMovieRepository(showtime_repo, cinema_repo)