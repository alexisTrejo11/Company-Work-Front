from ...core.entities.showtime import Showtime
from app.theater.application.repositories.theater_seat_repository import TheaterSeatRepository
from ..repositories.showtime_seat_repository import ShowtimeSeatRepository
from ...core.entities.showtime_seat import ShowtimeSeatEntity
from datetime import timezone, datetime

class ShowTimeSeatService:
    def __init__(self, theater_seat_repo: TheaterSeatRepository, showtime_seat_repo: ShowtimeSeatRepository):
        self.theater_seat_repo = theater_seat_repo
        self.showtime_seat_repo = showtime_seat_repo

    async def create_showtimes_seats(self, showtime: Showtime):
        theater_seats = await self.theater_seat_repo.get_by_theater(showtime.theater_id)
        showtimes_seats = self._generate_showtimes_seats(theater_seats, showtime)
        await self.showtime_seat_repo.bulk_create(showtimes_seats)

    def _generate_showtimes_seats(self, theater_seats, showtime):
        showtimes_seats = []
        for theater_seat in theater_seats:
            showtime_seat = ShowtimeSeatEntity(
                showtime_id=showtime.id,
                theater_seat_id=theater_seat.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            showtimes_seats.append(showtime_seat)
