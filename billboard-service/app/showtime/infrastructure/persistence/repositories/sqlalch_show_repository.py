from collections import defaultdict
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, delete
from app.shared.pagination import PaginationParams
from app.showtime.application.repositories.showtime_repository import ShowTimeRepository
from app.showtime.domain.entities.showtime import Showtime
from app.movies.application.dtos import ShowtimesByMovie, MovieShowtimesFilters
from ..mappers.showtime_mappers import ShowtimeModelMapper
from ..models.showtime_model import ShowtimeModel

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
            ShowtimeModel.start_time < normalized_end_time,
            ShowtimeModel.end_time > normalized_start_time
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
            model = await self.session.merge(model)
            
        await self.session.commit()
        
        if showtime.id is None:
            await self.session.refresh(model)

        return ShowtimeModelMapper.to_domain(model)


    async def delete(self, showtime_id: int) -> None:
        await self.session.execute(
            delete(ShowtimeModel).where(ShowtimeModel.id == showtime_id)
        )
        await self.session.commit()


    # MOVE?
    async def list_by_filters_group_by_movie(
        self, 
        showtime_filters: MovieShowtimesFilters, 
        page_params: PaginationParams
    ) -> Dict[int, List[Showtime]]:
        stmt = select(ShowtimeModel)
        
        filters = []
        
        if showtime_filters.incoming:
            filters.append(ShowtimeModel.start_time > datetime.now())
        if showtime_filters.cinema_id_list:
            filters.append(ShowtimeModel.cinema_id.in_(showtime_filters.cinema_id_list))
        if showtime_filters.movie_id:
            filters.append(ShowtimeModel.movie_id == showtime_filters.movie_id)
        
        if filters:
            stmt = stmt.where(and_(*filters))
        
        stmt = stmt.offset(page_params.offset).limit(page_params.limit)
        
        result = await self.session.execute(stmt)
        
        models = result.scalars().all()
        if not models:
            return {}            

        showtimes_by_movie = defaultdict(list)
        
        
        for model in models:
            showtimes_by_movie[model.movie_id].append(ShowtimeModelMapper.to_domain(model))
        
        return dict(showtimes_by_movie)