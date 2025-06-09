from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, status
from app.cinema.domain.entities import Cinema
from app.cinema.application.use_cases import GetCinemaByIdUseCase, GetActiveCinemasUseCase, SearchCinemasUseCase, CreateCinemaUseCase, UpdateCinemaUseCase, DeleteCinemaUseCase
from app.cinema.application.dtos.cinema_search import CinemaSearchFilters
from .depedencies import get_cinema_by_id_use_case, get_active_cinemas_use_case, search_cinemas_use_case, update_cinema_use_case, create_cinema_use_case, delete_cinema_use_case, get_filters

router = APIRouter(prefix="/api/v1/cinemas")

@router.get("/{cinema_id}", response_model=Cinema)
async def get_cinema_by_id(
    cinema_id: int,
    use_case: Annotated[GetCinemaByIdUseCase, Depends(get_cinema_by_id_use_case)]
):
    cinema = await use_case.execute(cinema_id)
    return cinema

@router.get("/active/", response_model=list[Cinema])
async def get_active_cinemas(
    use_case: Annotated[GetActiveCinemasUseCase, Depends(get_active_cinemas_use_case)]
):
    cinemas = await use_case.execute()
    return cinemas


@router.get("/", response_model=List[Cinema], summary="Search cinemas", description="Search cinemas with filtering and pagination")
async def search_cinemas(
    use_case: Annotated[SearchCinemasUseCase, Depends(search_cinemas_use_case)],
    filters: Annotated[CinemaSearchFilters, Depends(get_filters)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    page_params = {"offset": offset, "limit": limit}
    filter_params = filters.model_dump(exclude_none=True)
        
    cinemas = await use_case.execute(page_params, filter_params)
    return cinemas


@router.post("/", response_model=Cinema, status_code=status.HTTP_201_CREATED)
async def create_cinema(
    cinema: Cinema,
    use_case: Annotated[CreateCinemaUseCase, Depends(create_cinema_use_case)]
):
    created_cinema = await use_case.execute(cinema)
    return created_cinema
    

@router.put("/{cinema_id}", response_model=Cinema, status_code=status.HTTP_200_OK)
async def update_cinemas(
    cinema_id: int,
    cinema: Cinema,
    use_case: Annotated[UpdateCinemaUseCase, Depends(update_cinema_use_case)]
):
    created_cinema = await use_case.execute(cinema_id, cinema)
    return created_cinema


@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cinema(
    cinema_id: int,
    use_case: Annotated[DeleteCinemaUseCase, Depends(delete_cinema_use_case)]
):
    await use_case.execute(cinema_id)