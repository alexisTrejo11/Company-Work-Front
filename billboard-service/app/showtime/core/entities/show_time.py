from pydantic import Field, BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from .value_objects import ShowtimeLanguage, ShowtimeType, Seats
from ..exceptions.domain_exceptions import *

#TODO: Add New Fields to Model, Handle Seats, Add Repo missing func
class Showtime(BaseModel):
    """
    Represents a Showtime entity for a Movie in a Theater.
    """
    id: Optional[int] = None
    movie_id: int
    theater_id: int
    price: Decimal = Field(..., max_digits=6, decimal_places=2)
    start_time: datetime
    end_time: Optional[datetime] = None
    type: ShowtimeType
    language: ShowtimeLanguage
    total_seats: int
    avaialble_seats: int
    seats: List[Seats] = []

    _EXTRA_DURATIONS: Dict[str, int] = {
        "initial_cleaning": 10,
        "initial_commercials": 40,
        "post_credits_scene": 10,
        "post_cleaning": 30
    }
    
    @classmethod
    def get_buffered_extra_times(cls, include_post_credits_scene: bool = False) -> Dict[str, timedelta]:
        """
        Calculates the pre-show and post-show buffer durations.

        Args:
            include_post_credits_scene (bool): If True, adds time for post-credits scenes
                                               to the post-show buffer.

        Returns:
            Dict[str, timedelta]: A dictionary containing 'pre_buffer' and 'post_buffer'
                                  as timedelta objects.
        """
        pre_buffer_minutes = cls._EXTRA_DURATIONS["initial_cleaning"] + \
                             cls._EXTRA_DURATIONS["initial_commercials"]

        post_buffer_minutes = cls._EXTRA_DURATIONS["post_cleaning"]
        if include_post_credits_scene:
            post_buffer_minutes += cls._EXTRA_DURATIONS["post_credits_scene"]
        
        pre_buffer = timedelta(minutes=pre_buffer_minutes)
        post_buffer = timedelta(minutes=post_buffer_minutes)
        
        return {"pre_buffer": pre_buffer, "post_buffer": post_buffer}

    def validate_business_logic(self):
        """
        Validates the business rules for a Showtime entity.
        Raises custom domain exceptions if validation fails.
        """
        self._validate_price()
        self._validate_duration()
        self._validate_schedule_date()

    def update(self, new_data: 'Showtime'):
        self.start_time = new_data.start_time
        self.end_time = new_data.end_time
        self.price = new_data.price

    def take_seats(self, seats_number: int):
        self._validate_seat_quantity(seats_number)
        self._validate_avaliable_seats(seats_number)

        self.avaialble_seats -= seats_number

    def _validate_seat_quantity(self, seats_number: int):
        """
        Validates seats allowed range quantity  
        """
        MIN_SEAT_ALLOWED = 1
        MAX_SEAT_ALLOWED = 15
        
        if not MIN_SEAT_ALLOWED <= seats_number <= MAX_SEAT_ALLOWED:
            raise ShowtimeSeatsError(
                "Invalid seat quantity. " +
                f"Seat quantity must be between {MIN_SEAT_ALLOWED} to {MAX_SEAT_ALLOWED}"
            )

    def _validate_avaliable_seats(self, seats_number: int):
        """
        Validates enough quantity of a avaliable seats
        """
        if seats_number > self.avaialble_seats:
            raise ShowtimeSeatsError("No Seats Avaliable for requested operation")

    def _validate_price(self):
        """
        Validates that the showtime price is within the allowed limits.
        """
        MAX_LIMIT_PRICE = Decimal('50.00')
        MIN_LIMIT_PRICE = Decimal('3.00')

        if not (MIN_LIMIT_PRICE < self.price < MAX_LIMIT_PRICE): 
            raise InvalidShowtimePriceError(self.price, MIN_LIMIT_PRICE, MAX_LIMIT_PRICE)
        
    def _validate_schedule_date(self):
        """
        Validates that the showtime start_time is not in the past
        and is within a defined future limit (e.g., 30 days from now).
        """
        self._validate_not_schedule_in_past()
        self._validate_schedule_date_no_too_far()

    def _validate_duration(self):
        """
        Validates the showtime's duration, including start and end times.
        """
        MIN_SHOWTIME_DURATION_MINS = 30 # 0.5 hour (Supporting Short Films)
        MAX_SHOWTIME_DURATION_MINS = 300 # 5 hours (Supporting Sport Events)

        if not self.end_time:
            return

        if self.end_time <= self.start_time:
            raise ShowtimeSchedulingError("Showtime end time must be after start time.")

        duration_timedelta: timedelta = self.end_time - self.start_time
        duration_in_minutes = int(duration_timedelta.total_seconds() / 60)
        
        if not (MIN_SHOWTIME_DURATION_MINS <= duration_in_minutes <= MAX_SHOWTIME_DURATION_MINS):
            raise InvalidShowtimeDurationError(duration_in_minutes, MIN_SHOWTIME_DURATION_MINS, MAX_SHOWTIME_DURATION_MINS)
        
    def _validate_not_schedule_in_past(self):
        now_utc = datetime.now(datetime.timezone.utc)
        if self.start_time < now_utc:
            raise ShowtimeSchedulingError(
                f"Showtime start time '{self.start_time.isoformat()}' cannot be in the past relative to current time."
            )
        
    def _validate_schedule_date_no_too_far(self):
        MAX_DAYS_START_DATE_ALLOWED = 30
        now_utc = datetime.now(datetime.timezone.utc)
        future_limit_date = now_utc + timedelta(days=MAX_DAYS_START_DATE_ALLOWED)
        
        if self.start_time > future_limit_date:
            raise ShowtimeSchedulingError(
                f"Showtime start time '{self.start_time.isoformat()}' exceeds the maximum allowed future booking period of {MAX_DAYS_START_DATE_ALLOWED} days. "
                f"It must be before '{future_limit_date.isoformat()}'."
        )