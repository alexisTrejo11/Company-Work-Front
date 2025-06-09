from ..dtos.showtime_insert import ShowtimeCreate, ShowtimeUpdate
from ...domain.entities.showtime import Showtime as ShowtimeEntity
from datetime import datetime, timezone

class ShowtimeMappers:
    """
    Mapper class to convert between Showtime DTOs (Create/Update)
    and the Showtime domain entity.
    """

    @staticmethod
    def from_create_dto(create_data: ShowtimeCreate) -> ShowtimeEntity:
        """
        Converts a ShowtimeCreate DTO into a full Showtime domain entity
        for a new showtime.
        """
        now_utc = datetime.now(timezone.utc)
        
        return ShowtimeEntity(
            created_at=now_utc,
            updated_at=now_utc,
            total_seats=None, 
            available_seats=None,
            seats=[],
            **create_data.model_dump()
        )

    @staticmethod
    def update_with_dto(update_data: ShowtimeUpdate, existing_entity: ShowtimeEntity) -> ShowtimeEntity:
        updated_data = update_data.model_dump(exclude_unset=True, exclude={'id'})
        for key, value in updated_data.items():
            setattr(existing_entity, key, value)

        existing_entity.updated_at = datetime.now(timezone.utc)
        return existing_entity
