from typing import Optional, Dict, List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.movies.application.repositories import MovieRepository
from app.movies.domain.entities import Movie
from .models import MovieModel
from .mappers import MovieMapper

class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self,  session: AsyncSession):
        self.session = session

    async def get_active_movies(self) -> List[Movie]:        
        stmt = select(MovieModel).where(
            MovieModel.is_active == True
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [MovieMapper.to_entity(model) for model in models]

    async def get_by_id(self, movie_id: int) -> Optional[Movie]:
        model = await self.session.get(MovieModel, movie_id)
        if model:
            return MovieMapper.to_entity(model)
        return None

    async def get_all(self, page_params: Dict[str, int]) -> List[Movie]:
        offset = page_params.get('offset', 0)
        limit = page_params.get('limit', 10)
        
        stmt = select(MovieModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [MovieMapper.to_entity(model) for model in models]

    async def save(self, entity: Movie) -> Movie:
        model = MovieMapper.to_model(entity)
        
        if entity.id is None:
            self.session.add(model)
        else:
            model = await self.session.merge(model)
            
        await self.session.commit()
        
        if entity.id is None:
            await self.session.refresh(model)
        return MovieMapper.to_entity(model)

    
    async def delete(self, entity) -> None:
        stmt = delete(MovieModel).where(MovieModel.id == entity.id)
        await self.session.execute(stmt)
        await self.session.commit()


