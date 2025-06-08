from abc import ABC, abstractmethod
from ...core.entities.showtime_seat import ShowtimeSeatEntity as ShowtimeSeat
from typing import Optional, List

class ShowtimeSeatRepository:
    @abstractmethod
    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        pass

    @abstractmethod
    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        pass

    @abstractmethod
    async def get_by_id(self, seat_id: int) -> Optional[ShowtimeSeat]:
        pass

    @abstractmethod
    async def get_by_showtime_and_seat(self, showtime_id: int, seat_id: int) -> Optional[ShowtimeSeat]:
        pass

    @abstractmethod
    async def get_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        pass