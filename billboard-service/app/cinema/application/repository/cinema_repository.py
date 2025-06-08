from typing import Optional, List, Dict
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

    @abstractmethod
    async def search(self, page_params: Dict[str, int], filter_params: Dict[str, any]) -> List[Cinema]:
        """
        Perform a dynamic search of cinemas with pagination and filtering capabilities.
        
        Args:
            page_params: Dictionary containing pagination parameters (offset, limit)
            filter_params: Dictionary containing filter criteria for cinemas
            
        Returns:
            List of Cinema domain objects matching the criteria
        """
        pass