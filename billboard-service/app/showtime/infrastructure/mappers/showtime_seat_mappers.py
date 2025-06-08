from ..persistence.models.showtime_seat_model import ShowtimeSeatModel
from ...core.entities.showtime_seat import ShowtimeSeatEntity

class ShowTimeSeatModelMapper:

    @staticmethod
    def from_domain(entity: ShowtimeSeatEntity) -> ShowtimeSeatModel:
        dumped_data = entity.model_dump()
        return ShowtimeSeatModel(**dumped_data)

    @staticmethod
    def to_entity(model: ShowtimeSeatModel) -> ShowtimeSeatEntity:
        return ShowtimeSeatEntity.model_validate(model)
