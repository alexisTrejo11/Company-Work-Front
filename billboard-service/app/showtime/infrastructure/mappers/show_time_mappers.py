from ...core.entities.show_time import Showtime as ShowtimeEntity
from ..persistence.models.showtime_model import ShowtimeModel

class ShowtimeModelMapper:
    @staticmethod
    def from_domain(show_time_entity: ShowtimeEntity) -> ShowtimeModel:
        return ShowtimeModel(
            id=show_time_entity.id,
            movie_id=show_time_entity.movie_id,
            theater_id=show_time_entity.theater_id,
            start_time=show_time_entity.start_time,
            end_time=show_time_entity.end_time,
            price=show_time_entity.price
        )
    
    @staticmethod
    def to_domain(show_time_model: ShowtimeModel) -> ShowtimeEntity:
        if show_time_model is None:
            return None
            
        return ShowtimeEntity(
            id=show_time_model.id,
            movie_id=show_time_model.movie_id,
            theater_id=show_time_model.theater_id,
            start_time=show_time_model.start_time,
            end_time=show_time_model.end_time,
            price=show_time_model.price
        )