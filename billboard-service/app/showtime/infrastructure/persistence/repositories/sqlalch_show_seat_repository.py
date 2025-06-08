from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.showtime_seat_model import ShowtimeSeatModel
from ....application.repositories.showtime_seat_repository import ShowtimeSeatRepository
from ....core.entities.showtime_seat import ShowtimeSeatEntity as ShowtimeSeat
from ...mappers.showtime_seat_mappers import ShowTimeSeatModelMapper as ShowtimeSeatModelMapper

class SqlAlchShowtimeSeatRepository(ShowtimeSeatRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def bulk_create(self, seats: List[ShowtimeSeat]) -> None:
        seat_models = [ShowtimeSeatModelMapper.from_domain(seat) for seat in seats]
        
        self.session.add_all(seat_models)
        await self.session.commit()

    async def save(self, seat: ShowtimeSeat) -> ShowtimeSeat:
        seat_model = ShowtimeSeatModelMapper.from_domain(seat)
        
        if not seat.id:
            self.session.add(seat_model)
            await self.session.flush()
        else:
            seat_model = await self.session.merge(seat_model)

        await self.session.commit()
        await self.session.refresh(seat_model)

        return ShowtimeSeatModelMapper.to_domain(seat_model)

    async def get_by_id(self, seat_id: int) -> Optional[ShowtimeSeat]:
        result = await self.session.execute(
            select(ShowtimeSeatModel).where(
                ShowtimeSeatModel.id == seat_id
            )
        )
        model = result.scalars().first()
        
        return ShowtimeSeatModelMapper.to_domain(model) if model else None

    async def get_by_showtime_and_seat(self, showtime_id: int, theater_seat_id: int) -> Optional[ShowtimeSeat]:
        result = await self.session.execute(
            select(ShowtimeSeatModel).where( 
                ShowtimeSeatModel.showtime_id == showtime_id,
                ShowtimeSeatModel.theater_seat_id == theater_seat_id,
            )
        )
        model = result.scalars().first()
        
        return ShowtimeSeatModelMapper.to_domain(model) if model else None

    async def get_by_showtime(self, showtime_id: int) -> List[ShowtimeSeat]:
        result = await self.session.execute(
            select(ShowtimeSeatModel).where(
                ShowtimeSeatModel.showtime_id == showtime_id
            )
        )
        models = result.scalars().all()
        
        return [ShowtimeSeatModelMapper.to_domain(model) for model in models]