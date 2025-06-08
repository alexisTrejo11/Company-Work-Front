from typing import Optional, Dict, List
from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.cinema_model import CinemaModel
from ...mappers.cinema_mappers import CinemaModelMapper as CinemaMapper
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

    async def search(self, page_params: Dict[str, int], filter_params: Dict[str, any]) -> List[Cinema]:
        """
        Perform a dynamic search of cinemas with pagination and filtering capabilities.
        
        Args:
            page_params: Dictionary containing pagination parameters (offset, limit)
            filter_params: Dictionary containing filter criteria for cinemas
            
        Returns:
            List of Cinema domain objects matching the criteria
        """
        offset = page_params.get('offset', 0)
        limit = page_params.get('limit', 10)

        stmt = select(CinemaModel).offset(offset).limit(limit)
        
        if filter_params:
            filters = []
            
            if 'name' in filter_params:
                filters.append(CinemaModel.name.ilike(f"%{filter_params['name']}%"))
            if 'tax_number' in filter_params:
                filters.append(CinemaModel.tax_number == filter_params['tax_number'])
            if 'description' in filter_params:
                filters.append(CinemaModel.description.ilike(f"%{filter_params['description']}%"))
            
            if 'is_active' in filter_params:
                filters.append(CinemaModel.is_active == filter_params['is_active'])
            if 'has_parking' in filter_params:
                filters.append(CinemaModel.has_parking == filter_params['has_parking'])
            if 'has_food_court' in filter_params:
                filters.append(CinemaModel.has_food_court == filter_params['has_food_court'])
            
            if 'type' in filter_params:
                filters.append(CinemaModel.type == filter_params['type'])
            if 'status' in filter_params:
                filters.append(CinemaModel.status == filter_params['status'])
            if 'region' in filter_params:
                filters.append(CinemaModel.region == filter_params['region'])
            
            if 'min_screens' in filter_params:
                filters.append(CinemaModel.screens >= filter_params['min_screens'])
            if 'max_screens' in filter_params:
                filters.append(CinemaModel.screens <= filter_params['max_screens'])
            
            if 'renovated_after' in filter_params:
                filters.append(CinemaModel.last_renovation >= filter_params['renovated_after'])
            if 'renovated_before' in filter_params:
                filters.append(CinemaModel.last_renovation <= filter_params['renovated_before'])
            

            if 'latitude' in filter_params and 'longitude' in filter_params:
                filters.append(CinemaModel.latitude == filter_params['latitude'])
                filters.append(CinemaModel.longitude == filter_params['longitude'])
            
            if 'phone' in filter_params:
                filters.append(CinemaModel.phone == filter_params['phone'])
            if 'email_contact' in filter_params:
                filters.append(CinemaModel.email_contact.ilike(f"%{filter_params['email_contact']}%"))
            

            if filters:
                stmt = stmt.where(and_(*filters))
        
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
        return CinemaMapper.to_domain(model) if model else None

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
