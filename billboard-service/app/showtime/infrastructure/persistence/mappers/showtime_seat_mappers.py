from app.showtime.domain.entities.showtime_seat import ShowtimeSeat
from ...persistence.models.showtime_seat_model import ShowtimeSeatModel

class ShowtimeSeatModelMapper:

    @staticmethod
    def from_domain(entity: ShowtimeSeat) -> ShowtimeSeatModel:
        dumped_data = entity.model_dump()
        return ShowtimeSeatModel(**dumped_data)

    @staticmethod
    def to_entity(model: ShowtimeSeatModel) -> ShowtimeSeat:
        return ShowtimeSeat.model_validate(model)
