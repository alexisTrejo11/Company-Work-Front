from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, TYPE_CHECKING
import enum
from sqlalchemy import Enum as SqlEnum
from app.shared.base_model import Base 
    
if TYPE_CHECKING:
    from app.cinema.infrastructure.persistence.model.cinema_model import CinemaModel
    from app.showtime.infrastructure.persistence.models.showtime_model import ShowtimeModel

class TheaterTypeModel(enum.Enum):
    TWO_D = '2D'
    THREE_D = '3D'
    IMAX = 'IMAX'
    FOUR_DX = '4DX'
    VIP = 'V'

class TheaterModel(Base):
    __tablename__ = 'theaters'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey('cinemas.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    theater_type: Mapped[TheaterTypeModel] = mapped_column(
        SqlEnum(TheaterTypeModel, 
                name="theater_type_enum",
                create_type=False, 
                values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
        
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    maintenance_mode: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    cinema: Mapped["CinemaModel"] = relationship(back_populates="theaters")
    showtimes: Mapped[List["ShowtimeModel"]] = relationship(back_populates="theater")

    def __repr__(self) -> str:
        return f"<Theater(id={self.id}, name='{self.name}', type='{self.theater_type.value}')>"