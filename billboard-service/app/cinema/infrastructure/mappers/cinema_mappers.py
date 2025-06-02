from datetime import datetime
from ...core.entities.cinema import Cinema
from ...infrastructure.persistence.model.cinema_model import CinemaModel

class CinemaModelMapper:
    @staticmethod
    def from_domain(entity: Cinema) -> CinemaModel:
        if not isinstance(entity, Cinema):
            raise ValueError("Entity must be a Cinema instance")
            
        return CinemaModel(
            id=entity.id,
            name=entity.name,
            email_contact=entity.email_contact,
            tax_number=entity.tax_number,
            is_active=entity.is_active if entity.is_active is not None else False,
            created_at=entity.created_at or datetime.now(),
            updated_at=entity.updated_at or datetime.now()
        )

    @staticmethod
    def to_domain(model: CinemaModel) -> Cinema:
        if not isinstance(model, CinemaModel):
            raise ValueError("Model must be a CinemaModel instance")
            
        return Cinema(
            id=model.id,
            name=model.name,
            email_contact=model.email_contact,
            tax_number=model.tax_number,
            is_active=bool(model.is_active),
            created_at=model.created_at,
            updated_at=model.updated_at
        )