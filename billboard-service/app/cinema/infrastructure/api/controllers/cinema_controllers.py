from datetime import date
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.cinema.core.entities.valueobjects import LocationRegionEnum
from app.cinema.infrastructure.persistence.model.cinema_model import CinemaStatusEnum, CinemaTypeEnum
from ....core.entities.cinema import Cinema
from ....application.use_case.cinema_use_cases import GetCinemaByIdUseCase, GetActiveCinemasUseCase, SearchCinemasUseCase, CreateCinemaUseCase, UpdateCinemaUseCase, DeleteCinemaUseCase
from ...injection.depedencies import get_cinema_by_id_use_case, get_active_cinemas_use_case, search_cinemas_use_case, update_cinema_use_case, create_cinema_use_case, delete_cinema_use_case
from ....core.exceptions import CinemaNotFound

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
    name: Annotated[Optional[str], Query()] = None,
    tax_number: Annotated[Optional[str], Query()] = None,
    is_active: Annotated[Optional[bool], Query()] = None,
    min_screens: Annotated[Optional[int], Query(ge=0)] = None,
    max_screens: Annotated[Optional[int], Query(ge=0)] = None,
    type: Annotated[Optional[CinemaTypeEnum], Query()] = None,
    status: Annotated[Optional[CinemaStatusEnum], Query()] = None,
    region: Annotated[Optional[LocationRegionEnum], Query()] = None,
    has_parking: Annotated[Optional[bool], Query()] = None,
    has_food_court: Annotated[Optional[bool], Query()] = None,
    renovated_after: Annotated[Optional[date], Query()] = None,
    renovated_before: Annotated[Optional[date], Query()] = None,
    latitude: Annotated[Optional[float], Query()] = None,
    longitude: Annotated[Optional[float], Query()] = None,
    phone: Annotated[Optional[str], Query()] = None,
    email_contact: Annotated[Optional[str], Query()] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    try:
        page_params = {
            "offset": offset,
            "limit": limit
        }

        filter_params = {
            "name": name,
            "tax_number": tax_number,
            "is_active": is_active,
            "min_screens": min_screens,
            "max_screens": max_screens,
            "type": type,
            "status": status,
            "region": region,
            "has_parking": has_parking,
            "has_food_court": has_food_court,
            "renovated_after": renovated_after,
            "renovated_before": renovated_before,
            "latitude": latitude,
            "longitude": longitude,
            "phone": phone,
            "email_contact": email_contact
        }

        filter_params = {k: v for k, v in filter_params.items() if v is not None}

        cinemas = await use_case.execute(page_params, filter_params)
        return cinemas
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
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
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))