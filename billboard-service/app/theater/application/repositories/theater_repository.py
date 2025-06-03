from typing import List
from abc import abstractmethod
from ...core.entities.theater import Theater
from app.shared.repository.common_repository import CommonRepository

class TheaterRepository(CommonRepository[Theater]):
    @abstractmethod
    def get_by_cinema(self, cinema_id: int) -> List[Theater]:
        pass
