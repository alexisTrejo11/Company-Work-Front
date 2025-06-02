from sqlalchemy import String, Integer, Boolean, Date, DateTime
from sqlalchemy.orm import mapped_column, DeclarativeBase
from datetime import datetime, timezone 
import enum

class Base(DeclarativeBase):
    pass

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

    def __repr__(self):
        return f"<Cinema(id={self.id}, name='{self.name}', email='{self.email}')>"