from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Enum, Column, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.shared.base_model import Base 
from ....core.valueobjects.enums import SeatType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .theater_model import TheaterModel
    from app.showtime.infrastructure.persistence.models.showtime_seat_model import ShowtimeSeatModel
    
class TheaterSeatModel(Base):
    """
    SQLAlchemy ORM model for the 'theater_seats' table.
    """
    __tablename__ = 'theater_seats'

    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey('theaters.id', ondelete='CASCADE'), nullable=False)
    seat_row = Column(String(5), nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(Enum(SeatType, name='seat_type_enum', create_type=False), nullable=False, default=SeatType.STANDARD)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    theater = relationship('TheaterModel', back_populates="theater_seats")
    showtime_bookings = relationship("ShowtimeSeatModel", back_populates="theater_seat")

    __table_args__ = (
         UniqueConstraint('theater_id', 'seat_row', 'seat_number', name='uq_theater_seat_position'),
    )

    def __repr__(self):
        return f"<TheaterSeat(id={self.id}, theater_id={self.theater_id}, row='{self.seat_row}', number={self.seat_number}, type='{self.seat_type}')>"