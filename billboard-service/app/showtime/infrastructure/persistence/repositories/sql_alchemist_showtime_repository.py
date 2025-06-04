from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.showtime_model import ShowtimeModel
from ...mappers.show_time_mappers import ShowtimeModelMapper
from ....core.entities.show_time import Showtime
from app.shared.repository.common_repository import CommonRepository

class SQLAlchemyShowtimeRepository(CommonRepository[Showtime]):
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