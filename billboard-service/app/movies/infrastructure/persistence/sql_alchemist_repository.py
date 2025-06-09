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
        if entity.id:
          model = await self._update(entity)
        else:
            model = await self._create(entity)
        return MovieMapper.to_entity(model)

    async def _create(self, entity: Movie) -> MovieModel:
        model = MovieMapper.to_model(entity)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
    
    async def _update(self, entity: Movie):
        model = await self.session.get(MovieModel, entity.id)
        if not model:
            raise ValueError("Movie not found")
        
        model.title = entity.title
        model.original_title = entity.original_title
        model.duration = entity.duration
        model.release_date = entity.release_date
        model.end_date = entity.end_date
        model.description = entity.description
        model.genre = entity.genre
        model.rating = entity.rating
        model.poster_url = entity.poster_url
        model.trailer_url = entity.trailer_url
        model.is_active = entity.is_active

        await self.session.commit()
        await self.session.refresh(model)
    
    async def delete(self, entity) -> None:
        stmt = delete(MovieModel).where(MovieModel.id == entity.id)
        await self.session.execute(stmt)
        await self.session.commit()


