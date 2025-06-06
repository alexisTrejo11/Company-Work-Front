from abc import ABC, abstractmethod
from typing import List, Optional

from ...core.entities.seat import TheaterSeatEntity 

class TheaterSeatRepository(ABC):
    """
    Abstract Base Class for TheaterSeatRepository.
    Defines the contract for operations related to TheaterSeat entities.
    """

    @abstractmethod
    async def get_by_id(self, seat_id: int) -> Optional[TheaterSeatEntity]:
        """
        Retrieves a single TheaterSeatEntity by its unique ID.
        Args:
            seat_id: The ID of the theater seat.
        Returns:
            The TheaterSeatEntity if found, otherwise None.
        """
        pass

    @abstractmethod
    async def exist_by_theater_and_seat_values(self, theater_id: int, seat_row: str, seat_number: int) -> bool:        
        """
        Checks if a seat with the given theater_id, seat_row, and seat_number exists.
        """
        pass

    @abstractmethod
    async def get_by_theater(self, theater_id: int) -> List[TheaterSeatEntity]:
        """
        Retrieves all TheaterSeatEntities belonging to a specific theater.
        Args:
            theater_id: The ID of the theater.
        Returns:
            A list of TheaterSeatEntity objects.
        """
        pass

    @abstractmethod
    async def save(self, seat: TheaterSeatEntity) -> TheaterSeatEntity:
        """
        Saves a TheaterSeatEntity to the persistence layer.
        If the entity has an ID, it attempts to update an existing record.
        If the ID is None, it creates a new record.
        Args:
            seat: The TheaterSeatEntity object to save.
        Returns:
            The saved TheaterSeatEntity, potentially with an updated ID or timestamps.
        Raises:
            RuntimeError: If the save operation fails.
        """
        pass

    @abstractmethod
    async def delete(self, seat_id: int) -> None:
        """
        Deletes a TheaterSeatEntity by its unique ID.
        Args:
            seat_id: The ID of the theater seat to delete.
        """
        pass