from datetime import datetime, timedelta
from pydantic import Field, BaseModel
from decimal import Decimal
from typing import Optional
from ..exceptions.domain_exceptions import (
    InvalidShowtimePriceError,
    InvalidShowtimeDurationError,
    ShowtimeSchedulingError
)

class Showtime(BaseModel):
    """
    Represents a Showtime entity for a Movie in a Theater.
    """
    id: Optional[int] = None
    movie_id: int
    theater_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    price: Decimal = Field(..., max_digits=6, decimal_places=2)

    def validate_business_logic(self):
        """
        Validates the business rules for a Showtime entity.
        Raises custom domain exceptions if validation fails.
        """
        self._validate_price()
        self._validate_duration()
        self._validate_schedule_date()

    def _validate_price(self):
        """
        Validates that the showtime price is within the allowed limits.
        """
        MAX_LIMIT_PRICE = Decimal('50.00')
        MIN_LIMIT_PRICE = Decimal('3.00')

        if not (MIN_LIMIT_PRICE < self.price < MAX_LIMIT_PRICE): 
            raise InvalidShowtimePriceError(self.price, MIN_LIMIT_PRICE, MAX_LIMIT_PRICE)
        
    def update(self, new_data: 'Showtime'):
        self.start_time = new_data.start_time
        self.end_time = new_data.end_time
        self.price = new_data.price

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