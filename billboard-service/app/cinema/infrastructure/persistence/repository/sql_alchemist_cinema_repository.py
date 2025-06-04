from typing import Optional, Dict, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ...mappers.cinema_mappers import CinemaModelMapper as CinemaMapper
from ..model.cinema_model import CinemaModel
from ....application.repository.cinema_repository import CinemaRepository
from ....core.entities.cinema import Cinema
from ....core.exceptions import CinemaNotFound

class SQLAlchemyCinemaRepository(CinemaRepository):
    def __init__(self,  session: AsyncSession):
        self.session = session

    async def get_all(self, page_params: Dict[str, int]) -> List[Cinema]:
        offset = page_params.get('offset', 0)
        limit = page_params.get('limit', 10)
        
        stmt = select(CinemaModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [CinemaMapper.to_domain(model) for model in models]

    async def get_active_cinemas(self) -> List[Cinema]:
        stmt = select(CinemaModel).where(
            CinemaModel.is_active == True,
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [CinemaMapper.to_domain(model) for model in models]

    async def get_by_id(self, cinema_id: int) -> Optional[Cinema]:
        model = await self.session.get(CinemaModel, cinema_id)
        if model:
            return CinemaMapper.to_domain(model)
        return None
    
    async def get_cinemas_by_tax_number(self, tax_number: str) -> Optional[Cinema]: 
        stmt = select(CinemaModel).where(
            CinemaModel.tax_number == tax_number,
        )
        result = await self.session.execute(stmt)
        model = result.scalars().first()

        if not model:
            return None
        
        return CinemaMapper.to_domain(model) 

    async def save(self, entity: Cinema) -> Cinema:
        if entity.id:
          model = await self._update(entity)
        else:
            model = await self._create(entity)
        return CinemaMapper.to_domain(model)

    async def _create(self, entity: Cinema) -> CinemaModel:
        model = CinemaMapper.from_domain(entity)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
    
    async def _update(self, entity: Cinema) -> CinemaModel:
        model = await self.session.get(CinemaModel, entity.id)
        
        if not model:
            raise CinemaNotFound(f"Cinema with ID {entity.id} not found for update.")

        entity_data = CinemaMapper.from_domain(entity).__dict__
        keys_to_exclude = {'id', 'created_at', '_sa_instance_state'}
        
        for key, value in entity_data.items():
            if key not in keys_to_exclude:
                setattr(model, key, value)
        
        await self.session.commit()
        await self.session.refresh(model) 
        
        return model

    async def delete(self, entity) -> None:
        stmt = delete(CinemaModel).where(CinemaModel.id == entity.id)
        await self.session.execute(stmt)
        await self.session.commit()


