from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Numeric, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func
from app.shared.base_model import Base
from app.showtime.domain.enums import ShowtimeLanguage, ShowtimeType

if TYPE_CHECKING:
    from app.movies.infrastructure.persistence.models import MovieModel
    from app.theater.infrastructure.persistence.models.theater_model import TheaterModel
    from app.cinema.infrastructure.persistence.cinema_model import CinemaModel
    from ..models.showtime_seat_model import ShowtimeSeatModel
    
class  ShowtimeModel(Base):
    __tablename__ = 'showtimes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id'), nullable=False)
    theater_id: Mapped[int] = mapped_column(ForeignKey('theaters.id'), nullable=False)
    cinema_id: Mapped[int] = mapped_column(ForeignKey('cinemas.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    language: Mapped[ShowtimeLanguage] = mapped_column(Enum(ShowtimeLanguage, name='showtime_language_enum', create_type=False), nullable=False)
    type: Mapped[ShowtimeType] = mapped_column(Enum('TRADITIONAL_2D', 'TRADITIONAL_3D', 'IMAX_2D', 'IMAX_3D', '4D', '4DX', 'VIP_2D', 'VIP_3D', name='showtime_type_enum',create_type=False),nullable=False) # Can't Check Enums Values Cause Naming
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    movie: Mapped["MovieModel"] = relationship(back_populates="showtimes")
    theater: Mapped["TheaterModel"] = relationship(back_populates="showtimes")
    showtime_seats: Mapped["ShowtimeSeatModel"] = relationship(back_populates="showtimes")
    cinema: Mapped["CinemaModel"] = relationship(back_populates="showtimes")

    def __repr__(self) -> str:
        return f"<Showtime(id={self.id}, movie_id={self.movie_id}, theater_id={self.theater_id}, start_time='{self.start_time}')>"