from ...core.entities.theater import Theater as TheaterEntity, TheaterType as TheaterTypeEntity
from ..persistence.models.theater_model import TheaterModel, TheaterTypeModel

class TheaterModelMapper:
    @staticmethod
    def from_domain(theater_entity: TheaterEntity) -> TheaterModel:
        return TheaterModel(
            id=theater_entity.id if theater_entity.id else None,
            cinema_id=theater_entity.cinema_id,
            name=theater_entity.name,
            capacity=theater_entity.capacity,

            theater_type=TheaterTypeModel(theater_entity.theater_type),
            is_active=theater_entity.is_active,
            maintenance_mode=theater_entity.maintenance_mode
        )
    
    @staticmethod
    def to_domain(theater_model: TheaterModel) -> TheaterEntity:
        if theater_model is None:
            return None

        return TheaterEntity(
            id=theater_model.id,
            cinema_id=theater_model.cinema_id,
            name=theater_model.name,
            capacity=theater_model.capacity,
            theater_type=TheaterTypeEntity(theater_model.theater_type.value),
            is_active=theater_model.is_active,
            maintenance_mode=theater_model.maintenance_mode
        )