from datetime import datetime, timezone
from typing import Dict, Any
from app.showtime.domain.entities.showtime import Showtime
from app.showtime.application.dtos.showtime_insert import ShowtimeCreate, ShowtimeUpdate
from ...persistence.models.showtime_model import ShowtimeModel

class ShowtimeModelMapper:
    """
    Mapper class to convert between ShowtimeEntity (domain),
    ShowtimeCreate/Update DTOs, and ShowtimeModel (persistence/ORM).
    """

    @staticmethod
    def from_domain(entity: Showtime) -> ShowtimeModel:
        """
        Converts a ShowtimeEntity domain object to a ShowtimeModel ORM object.
        Used when saving/updating data in the database.
        Note: total_seats, available_seats, and seats are domain-only properties
        and are not directly mapped to the database model.
        """
        dumped_data = entity.model_dump(
            exclude_none=True,
            exclude={
                'total_seats',
                'available_seats',
                'seats'
            }
        )
        return ShowtimeModel(**dumped_data)

    @staticmethod
    def to_domain(model: ShowtimeModel) -> Showtime:
        """
        Converts a ShowtimeModel ORM object to a ShowtimeEntity domain object.
        Used when retrieving data from the database for application logic.
        Note: total_seats, available_seats, and seats need to be populated by
        separate logic (e.g., in a use case) if they are derived.
        Here, they will be set to their default values (e.g., None, 0, []).
        """
        if model is None:
            return None
        
        return Showtime.model_validate(model)

    @staticmethod
    def from_create_dto(dto: ShowtimeCreate) -> ShowtimeModel:
        """
        Converts a ShowtimeCreate DTO to a ShowtimeModel ORM object for insertion.
        Sets created_at and updated_at to the current UTC time.
        """
        now_utc = datetime.now(timezone.utc)
        
        return ShowtimeModel(
            created_at=now_utc,
            updated_at=now_utc,
            **dto.model_dump()
        )

    @staticmethod
    def from_update_dto(dto: ShowtimeUpdate) -> Dict[str, Any]:
        """
        Converts a ShowtimeUpdate DTO to a dictionary of fields to update.
        Uses exclude_unset=True for partial updates.
        This dictionary can then be applied to an existing ShowtimeModel instance.
        """
        update_data = dto.model_dump(
            exclude_unset=True,
            exclude={'id'}
        )

        update_data['updated_at'] = datetime.now(timezone.utc)
        
        return update_data