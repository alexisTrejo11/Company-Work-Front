from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ...injection.depedencies import get_cinema_by_id_use_case, get_active_cinemas_use_case, search_cinemas_use_case, update_cinema_use_case, create_cinema_use_case, delete_cinema_use_case, get_filters
from ....core.entities.cinema import Cinema
from ....core.exceptions import CinemaNotFound
from ....application.use_case.cinema_use_cases import GetCinemaByIdUseCase, GetActiveCinemasUseCase, SearchCinemasUseCase, CreateCinemaUseCase, UpdateCinemaUseCase, DeleteCinemaUseCase
from ....application.dtos.cinema_search_dtos import CinemaSearchFilters

router = APIRouter(prefix="/api/v1/cinemas")

@router.get("/{cinema_id}", response_model=Cinema)
async def get_cinema_by_id(
    cinema_id: int,
    use_case: Annotated[GetCinemaByIdUseCase, Depends(get_cinema_by_id_use_case)]
):
    try:
        cinema = await use_case.execute(cinema_id)
        return cinema
    except CinemaNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cinema not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/active/", response_model=list[Cinema])
async def get_active_cinemas(
    use_case: Annotated[GetActiveCinemasUseCase, Depends(get_active_cinemas_use_case)]
):
    try:
        cinemas = await use_case.execute()
        return cinemas
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[Cinema], summary="Search cinemas", description="Search cinemas with filtering and pagination")
async def search_cinemas(
    use_case: Annotated[SearchCinemasUseCase, Depends(search_cinemas_use_case)],
    filters: Annotated[CinemaSearchFilters, Depends(get_filters)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    try:
        page_params = {"offset": offset, "limit": limit}
        filter_params = filters.model_dump(exclude_none=True)
        
        cinemas = await use_case.execute(page_params, filter_params)
        return cinemas
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/", response_model=Cinema, status_code=status.HTTP_201_CREATED)
async def create_cinema(
    cinema: Cinema,
    use_case: Annotated[CreateCinemaUseCase, Depends(create_cinema_use_case)]
):
    try:
        created_cinema = await use_case.execute(cinema)
        return created_cinema
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.put("/{cinema_id}", response_model=Cinema, status_code=status.HTTP_200_OK)
async def update_cinemas(
    cinema_id: int,
    cinema: Cinema,
    use_case: Annotated[UpdateCinemaUseCase, Depends(update_cinema_use_case)]
):
    try:
        created_cinema = await use_case.execute(cinema_id, cinema)
        return created_cinema
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cinema(
    cinema_id: int,
    use_case: Annotated[DeleteCinemaUseCase, Depends(delete_cinema_use_case)]
):
    try:
        await use_case.execute(cinema_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))