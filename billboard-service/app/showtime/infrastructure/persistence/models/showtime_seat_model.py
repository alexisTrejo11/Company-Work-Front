from __future__ import annotations
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.shared.base_model import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .showtime_model import ShowtimeModel
    from app.theater.infrastructure.persistence.models.theater_seat_model import TheaterSeatModel

class ShowtimeSeatModel(Base):
    """
    SQLAlchemy ORM model for the 'showtime_seats' table.
    """
    __tablename__ = 'showtime_seats'

    id = Column(Integer, primary_key=True, index=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.id', ondelete='CASCADE'), nullable=False)
    theater_seat_id = Column(Integer, ForeignKey('theater_seats.id', ondelete='RESTRICT'), nullable=False)
    taken_at = Column(DateTime(timezone=True), nullable=True)
    transaction_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    showtimes = relationship("ShowtimeModel", back_populates="showtime_seats")
    theater_seat = relationship("TheaterSeatModel", back_populates="showtime_bookings")

    __table_args__ = (
        UniqueConstraint('showtime_id', 'theater_seat_id', name='uq_showtime_seat'),
    )

    def __repr__(self):
        return (
            f"<ShowtimeSeat(id={self.id}, showtime_id={self.showtime_id}, "
            f"theater_seat_id={self.theater_seat_id}, taken_at={self.taken_at})>"
        )