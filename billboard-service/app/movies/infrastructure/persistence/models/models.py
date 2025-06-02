from sqlalchemy import String, Integer, Boolean, Date, DateTime
from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass

class MovieModel(Base):
    __tablename__ = 'movies'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(200), nullable=False)
    original_title = mapped_column(String(200))
    minute_duration = mapped_column(Integer, nullable=False)
    release_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)
    description = mapped_column(String, nullable=False)
    genre = mapped_column(String, nullable=False)
    rating = mapped_column(String, nullable=False)
    poster_url = mapped_column(String)
    trailer_url = mapped_column(String)
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())