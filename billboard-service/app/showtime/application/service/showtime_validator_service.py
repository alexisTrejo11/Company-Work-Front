from ...core.entities.showtime import Showtime
from app.shared.exceptions import ValidationException
from app.theater.application.repositories.theater_seat_repository import TheaterSeatRepository
from ..repositories.showtime_repository import ShowTimeRepository

#TODO: Validation To Specfic Exception
class ShowtimeValidationService:
    def __init__(self, showtime_repo: ShowTimeRepository, theater_seat_repo:TheaterSeatRepository):
        self.showtime_repo = showtime_repo
        self.theater_seat_repo = theater_seat_repo

    async def validate_insert(self,  proposed_showtime: Showtime, has_post_credits: bool):
        # Exclude in update
        # Add Status Validation
        await self.validation_service.validate_no_overlap(proposed_showtime, has_post_credits)
        await self.validation_service.validate_theater_seats(proposed_showtime.theater_id)


    async def validate_theater_seats(self, theater_id):
        theater_count = self.theater_seat_repo.count_by_theater(theater_id)
        if theater_count == 0:
            raise ValidationException("Theater don't have seats can't create showtime")

    async def validate_no_overlap(self, proposed_showtime: Showtime, include_post_credits_scene: bool = False):
        """
        Validates if a proposed showtime conflicts with any existing showtimes
        in the same theater, considering pre and post buffers.

        Args:
            proposed_showtime (Showtime): The new showtime being proposed.
            include_post_credits_scene (bool): Whether to include post-credits scene
                                               duration in the end time buffer.

        Raises:
            ValidationException: If the proposed showtime overlaps with an existing one.
        """
        buffers = Showtime.get_buffered_extra_times(include_post_credits_scene)
        pre_buffer = buffers["pre_buffer"]
        post_buffer = buffers["post_buffer"]

        buffered_start_time = proposed_showtime.start_time - pre_buffer
        buffered_end_time = proposed_showtime.end_time + post_buffer
        
        if not proposed_showtime.id:
            overlapping_showtime = await self.showtime_repo.get_by_theater_and_date_range(
                theater_id=proposed_showtime.theater_id,
                start_time_to_check=buffered_start_time,
                end_time_to_check=buffered_end_time
            )
        else:
            overlapping_showtime = await self.showtime_repo.get_by_theater_and_date_range(
                theater_id=proposed_showtime.theater_id,
                start_time_to_check=buffered_start_time,
                end_time_to_check=buffered_end_time,
                exclude_showtime_id=proposed_showtime.id
            )

        if overlapping_showtime:
            raise ValidationException(
                f"Can't schedule Showtime (ID: {proposed_showtime.id}). "
                f"It overlaps with existing Showtime {overlapping_showtime.id} "
                f"in Theater {proposed_showtime.theater_id}. "
                f"Proposed buffered range: {buffered_start_time.strftime('%H:%M')} - {buffered_end_time.strftime('%H:%M')}"
            )
    