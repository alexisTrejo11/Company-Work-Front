from __future__ import annotations
from sqlalchemy import Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy.sql import func
from decimal import Decimal
from app.shared.base_model import Base

if TYPE_CHECKING:
    from app.movies.infrastructure.persistence.models.models import MovieModel
    from app.theater.infrastructure.persistence.models.theater_model import TheaterModel


class ShowtimeModel(Base):
    __tablename__ = 'showtimes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id'), nullable=False)
    theater_id: Mapped[int] = mapped_column(ForeignKey('theaters.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    movie: Mapped["MovieModel"] = relationship(back_populates="showtimes")
    theater: Mapped["TheaterModel"] = relationship(back_populates="showtimes")

    def __repr__(self) -> str:
        return f"<Showtime(id={self.id}, movie_id={self.movie_id}, theater_id={self.theater_id}, start_time='{self.start_time}')>"