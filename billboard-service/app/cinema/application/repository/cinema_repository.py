from typing import Optional, List
from abc import abstractmethod, ABC
from ...core.entities.cinema import Cinema
from app.shared.repository.common_repository import CommonRepository

class CinemaRepository(CommonRepository[Cinema], ABC):
    """
    Specific repository interface for Cinema entities.
    Inherits common CRUD methods for Cinema.
    """
    @abstractmethod
    async def get_cinemas_by_tax_number(self, tax_number: str) -> Optional[Cinema]:
        pass
    

    @abstractmethod
    async def get_active_cinemas(self, tax_number: str) -> List[Cinema]:
        pass