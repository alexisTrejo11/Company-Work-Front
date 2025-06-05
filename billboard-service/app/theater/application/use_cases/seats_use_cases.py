from typing import List, Optional
from app.shared.exceptions import NotFoundException
from ...core.entities.seat import TheaterSeatEntity
from ...application.repositories.theater_seat_repository import TheaterSeatRepository
from ...application.repositories.theater_repository import TheaterRepository

class GetTheaterSeatByIdUseCase:
    """
    Use case to retrieve a single theater seat by its ID.
    """
    def __init__(self, repository: TheaterSeatRepository):
        self.repository = repository

    async def execute(self, seat_id: int) -> Optional[TheaterSeatEntity]:
        """
        Executes the use case to find a theater seat.

        Args:
            seat_id: The unique identifier of the theater seat.

        Returns:
            The TheaterSeatEntity if found, otherwise None.
        """
        seat = await self.repository.get_by_id(seat_id)
        if not seat:
            raise NotFoundException("Seat", seat_id)

        return seat

class GetSeatsByTheaterUseCase:
    """
    Use case to retrieve all theater seats for a specific theater.
    """
    def __init__(self, seat_repository: TheaterSeatRepository, theater_repository: TheaterRepository):
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    async def execute(self, theater_id: int) -> List[TheaterSeatEntity]:
        """
        Executes the use case to find all seats in a given theater.

        Args:
            theater_id: The unique identifier of the theater.

        Returns:
            A list of TheaterSeatEntity objects.
        """
        theater = await self.theater_repository.get_by_id(theater_id)
        if not theater:
            raise NotFoundException("Theater", theater_id)

        return await self.seat_repository.get_by_theater(theater_id)

class SaveTheaterSeatUseCase:
    """
    Use case to save (create or update) a theater seat.
    """
    def __init__(self, seat_repository: TheaterSeatRepository, theater_repository: TheaterRepository):
        self.seat_repository = seat_repository
        self.theater_repository = theater_repository

    async def execute(self, seat: TheaterSeatEntity) -> TheaterSeatEntity:
        """
        Executes the use case to save a theater seat.
        This handles both creation (if seat.id is None) and updating.

        Args:
            seat: The TheaterSeatEntity object to be saved.

        Returns:
            The saved TheaterSeatEntity (with potentially new ID/timestamps if created).

        Raises:
            RuntimeError: If the save operation fails at the repository level.
        """
        theater_id = seat.theater_id
        
        theater = await self.theater_repository.get_by_id(theater_id)
        if not theater:
            raise NotFoundException("Theater", theater_id)

        return await self.seat_repository.save(seat)

class DeleteTheaterSeatUseCase:
    """
    Use case to delete a theater seat by its ID.
    """
    def __init__(self, repository: TheaterSeatRepository):
        self.repository = repository

    async def execute(self, seat_id: int) -> None:
        """
        Executes the use case to delete a theater seat.

        Args:
            seat_id: The unique identifier of the theater seat to delete.
        """
        theater = await self.repository.get_by_id(seat_id)
        if not theater:
            raise NotFoundException("Seat", seat_id)
        
        await self.repository.delete(seat_id)