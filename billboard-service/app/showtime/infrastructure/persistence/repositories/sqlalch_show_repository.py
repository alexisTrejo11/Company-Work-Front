from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.showtime_model import ShowtimeModel
from ...mappers.showtime_mappers import ShowtimeModelMapper
from ....core.entities.showtime import Showtime
from ....application.repositories.showtime_repository import ShowTimeRepository


class SQLAlchemyShowtimeRepository(ShowTimeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, showtime_id: int) -> Optional[Showtime]:
        result = await self.session.execute(
            select(ShowtimeModel).where(ShowtimeModel.id == showtime_id)
        )
        model = result.scalars().first()
        return ShowtimeModelMapper.to_domain(model) if model else None

    async def get_all(self, page_params: Dict[str, int]) -> List[Showtime]:
        offset = page_params.get('offset', 0)
        limit = page_params.get('limit', 100)
        
        result = await self.session.execute(
            select(ShowtimeModel)
            .offset(offset)
            .limit(limit)
            .order_by(ShowtimeModel.start_time)
        )
        return [ShowtimeModelMapper.to_domain(model) for model in result.scalars()]

    async def get_incoming_by_cinema(self, cinema_id:int) -> List[Showtime]:
        now_utc = datetime.now(timezone.utc)
        end_of_current_day_boundary_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        query = select(ShowtimeModel).where(
            ShowtimeModel.cinema_id == cinema_id,
            ShowtimeModel.start_time >= now_utc,
            ShowtimeModel.start_time < end_of_current_day_boundary_utc, 
        )
        
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [ShowtimeModelMapper.to_domain(model) for model in models]

    async def get_incoming_by_movie(self, movie_id:int) -> List[Showtime]:
        now_utc = datetime.now(timezone.utc)
        end_of_current_day_boundary_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        query = select(ShowtimeModel).where(
            ShowtimeModel.movie_id == movie_id,
            ShowtimeModel.start_time >= now_utc,
            ShowtimeModel.start_time < end_of_current_day_boundary_utc, 
        )
        
        result = await self.session.execute(query)
        models = result.scalars().all()

        return [ShowtimeModelMapper.to_domain(model) for model in models]

    async def get_incoming_movie_showtimes(self, movie_id: int = None, cinema_id: int = None) -> Dict[int, Showtime]:
        """
        TODO: move to specific repo
        DICT --> {key: movie_id: value: [...showtime]}
        """
        pass

    async def get_by_theater_and_date_range(
        self,
        theater_id: int,
        start_time_to_check: datetime,
        end_time_to_check: datetime,
        exclude_showtime_id: Optional[int] = None
    ) -> List[Showtime]:
        """
        Retrieves showtimes for a given theater within a specified date/time range.
        Optionally excludes a specific showtime by ID.

        """
        def _normalize_dt(dt: datetime) -> datetime:
            return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

        normalized_start_time = _normalize_dt(start_time_to_check)
        normalized_end_time = _normalize_dt(end_time_to_check)

        query = select(ShowtimeModel).where(
            ShowtimeModel.theater_id == theater_id,
            # Showtime starts within the check range / Add Endtime restriction ??
            ShowtimeModel.start_time >= normalized_start_time,
            ShowtimeModel.start_time <= normalized_end_time,
        
        )
        if exclude_showtime_id is not None:
            query = query.where(ShowtimeModel.id != exclude_showtime_id)

        result = await self.session.execute(query)
        models = result.scalars().all()
        
        return [ShowtimeModelMapper.to_domain(model) for model in models]

    async def save(self, showtime: Showtime) -> Showtime:
        model = ShowtimeModelMapper.from_domain(showtime)
        
        if showtime.id is None:
            self.session.add(model)
        else:
            await self.session.merge(model)
            
        await self.session.commit()
        await self.session.refresh(model)
        return ShowtimeModelMapper.to_domain(model)

    async def delete(self, showtime_id: int) -> None:
        await self.session.execute(
            delete(ShowtimeModel).where(ShowtimeModel.id == showtime_id)
        )
        await self.session.commit()