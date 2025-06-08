from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, DateTime, Date, Text, Float, ARRAY, Enum as SQLEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime, date, timezone
import enum
from app.shared.base_model import Base
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.theater.infrastructure.persistence.models.theater_model import TheaterModel
    from app.showtime.infrastructure.persistence.models.showtime_model import ShowtimeModel

class CinemaStatusEnum(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    MAINTENANCE = "MAINTENANCE"

class CinemaTypeEnum(enum.Enum):
    VIP = "VIP"
    TRADITIONAL = "TRADITIONAL"

class CinemaFeaturesEnum(enum.Enum):
    TWO_D = "2D"
    THREE_D = "3D"
    FOUR_D = "4D"
    IMAX = "IMAX"
    VIP_SEATING = "VIP_SEATING"
    DOBLY_ATMOS = "DOBLY_ATMOS"


class CinemaModel(Base):
    __tablename__ = 'cinemas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Cinema Info
    image: Mapped[str] = mapped_column(Text, nullable=False, default='')
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    tax_number: Mapped[str] = mapped_column(String(255), nullable=False, unique=True) # Updated length
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default='')
    screens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Dates/Timestamps
    last_renovation: Mapped[Optional[date]] = mapped_column(Date, nullable=True) # Using Date for just date
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Enums
    type: Mapped[CinemaTypeEnum] = mapped_column(SQLEnum(CinemaTypeEnum, name='cinema_type_enum', create_type=False), nullable=False)
    status: Mapped[CinemaStatusEnum] = mapped_column(SQLEnum(CinemaStatusEnum, name='cinema_status_enum', create_type=False), nullable=False)

    # Amenities
    has_parking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_food_court: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_coffee_station: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_disabled_access: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Contact Info
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email_contact: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Location
    latitude: Mapped[float] = mapped_column(Float(precision=53), nullable=False)
    longitude: Mapped[float] = mapped_column(Float(precision=53), nullable=False)

    # Social Media URLs
    facebook_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instagram_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    x_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tik_tok_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Features 
    features: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False, default=[])

    theaters: Mapped[List["TheaterModel"]] = relationship(
        back_populates="cinema",
        cascade="all, delete-orphan"
    )

    showtimes: Mapped[List["ShowtimeModel"]] = relationship(
        back_populates="cinema",
    )

    def __repr__(self):
        return (
            f"<CinemaModel(id={self.id}, name='{self.name}', status='{self.status.value}', "
            f"latitude={self.latitude}, longitude={self.longitude})>"
        )