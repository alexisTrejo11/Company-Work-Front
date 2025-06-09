from .dtos.cinema_insert import CinemaCreate, CinemaUpdate
from ..domain.entities import Cinema

class CinemaMapper:

    @staticmethod
    def from_create_dto(cinema_create: CinemaCreate) -> Cinema:
        return Cinema(**cinema_create.model_dump())
    
    @staticmethod
    def update_cinema_from_dto(existing_cinema: Cinema, cinema_update: CinemaUpdate) -> Cinema:
        update_data = cinema_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(existing_cinema, key, value)

        return existing_cinema