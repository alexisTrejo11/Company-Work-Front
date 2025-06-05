from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ....core.entities.theater import Theater
from ...persistence.models.theater_seat_model import TheaterSeatModel
from ...mappers.theater_seat_mappers import TheaterSeatModelMapper
from ....application.repositories.theater_seat_repository import TheaterSeatRepository

class SqlAlchemistTheaterSeatRepository(TheaterSeatRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, seat_id: int) -> Optional[Theater]:
        result = await self.session.execute(
            select(TheaterSeatModel).where(TheaterSeatModel.id == seat_id)
        )
        model = result.scalars().first()
        return TheaterSeatModelMapper.to_domain(model) if model else None

    async def get_by_theater(self, theater_id: int) -> List[Theater]:
        result = await self.session.execute(
            select(TheaterSeatModel).where(TheaterSeatModel.theater_id == theater_id)
        )
        models = result.scalars().all()        
        return [TheaterSeatModelMapper.to_domain(model) for model in models]

    async def save(self, theater: Theater) -> Theater:
        model = TheaterSeatModelMapper.from_domain(theater)
        
        try:
            if theater.id is None:
                self.session.add(model)
                await self.session.flush()
            else:
                model = await self.session.merge(model)
            
            await self.session.commit()
            
            if model in self.session:
                await self.session.refresh(model)
                
            return TheaterSeatModelMapper.to_domain(model)
            
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Failed to save seat: {str(e)}") from e

    async def delete(self, seat_id: int) -> None:
        await self.session.execute(
            delete(TheaterSeatModel).where(TheaterSeatModel.id == seat_id)
        )
        await self.session.commit()