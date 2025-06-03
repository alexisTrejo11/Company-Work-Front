from __future__ import annotations
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime, timezone
import enum
from app.shared.base_model import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.theater.infrastructure.persistence.models.theater_model import TheaterModel

class CinemaStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class CinemaModel(Base):
    __tablename__ = 'cinemas'

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(255), nullable=False, unique=True)
    email_contact = mapped_column(String(255), nullable=False, unique=True)
    tax_number = mapped_column(String(255), nullable=False, unique=True)
    is_active = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    theaters: Mapped[List["TheaterModel"]] = relationship(
        back_populates="cinema"
    )

    def __repr__(self):
        return f"<Cinema(id={self.id}, name='{self.name}', email='{self.email}')>"